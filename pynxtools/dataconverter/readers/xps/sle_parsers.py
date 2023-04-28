"""Parsers for reading loading XPS (X-ray Photoelectron Spectroscopy) data
 from Specs Lab Prodigy, to be passed to mpes nxdl (NeXus Definition Language)
 template.
"""
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sqlite3
from datetime import datetime
import xml.etree.ElementTree as ET
import struct
from copy import copy
import numpy as np
import re
import os


class SleParser():
    """
    Generic parser without reading capabilities,
    to be used as template for implementing parsers for different versions.
    """

    def __init__(self):
        self.con = ''
        self.spectra = []

        self.keys_map = {
            'Udet': 'detector_voltage',
            'Comment': 'comments',
            'ElectronEnergy': 'start_energy',
            'SpectrumID': 'spectrum_id',
            'EpassOrRR': 'pass_energy',
            'EnergyType': 'x_units',
            'Samples': 'n_values',
            'Wf': 'workfunction',
            'Step': 'step',
            'Ubias': 'electron_bias',
            'DwellTime': 'dwell_time',
            'NumScans': 'scans',
            'LensMode': 'lens_mode',
            'Timestamp': 'time_stamp',
            'Entrance': 'entrance_slit',
            'Exit': 'exit_slit',
            'ScanMode': 'scan_mode',
            'VoltageRange': 'voltage_range',
        }

        self.spectrometer_setting_map = {
            'Coil Current [mA]': 'coil_current',
            'Pre Defl Y [nU]': 'y_deflector',
            'Pre Defl X [nU]': 'x_deflector',
            'L1 [nU]': 'lens1',
            'L2 [nU]': 'lens2',
            'Focus Displacement 1 [nu]': 'focus_displacement',
            'Detector Voltage [V]': 'detector_voltage',
            'Bias Voltage Electrons [V]': 'bias_voltage_electrons',
            'Bias Voltage Ions [V]': 'bias_voltage_ions',
        }

        self.source_setting_map = {
            'anode': 'source_label',
            'uanode': 'source_voltage',
            'iemission': 'emission_current',
            'DeviceExcitationEnergy': 'excitation_energy',
        }

        self.sql_metadata_map = {
            'EnergyType': 'x_units',
            'EpassOrRR': 'pass_energy',
            'Wf': 'workfunction',
            'Timestamp': 'time_stamp',
            'Samples': 'n_values',
            'ElectronEnergy': 'start_energy',
            'Step': 'step_size',
        }

        self.key_maps = [
            self.keys_map,
            self.spectrometer_setting_map,
            self.source_setting_map,
            self.sql_metadata_map,
        ]

        self.value_map = {
            'x_units': self._change_energy_type,
            'time_stamp': self._convert_date_time,
        }

        self.keys_to_drop = [
            'CHANNELS_X',
            'CHANNELS_Y',
            # 'Bias Voltage Ions [V]',
            'operating_mode',
        ]

        self.encodings_map = {
            'double': ['d', 8],
            'float': ['f', 4],
        }

        self.encoding = ['f', 4]

        self.average_scans = True

        self.spectrometer_types = ['Phoibos1D']

        self.measurement_types = ['XPS', 'UPS', 'ElectronSpectroscopy']

    def initiate_file_connection(self, filename):
        """Set the filename of the file to be opened."""
        self.sql_connection = filename
        self.con = sqlite3.connect(self.sql_connection)
        self.spectrum_column_names = self._get_column_names('Spectrum')

    def set_current_file(self, filepath):
        """
        Set the filename of the file to be opened.

        Parameters
        ----------
        filename : str
            Filepath of the SLE file to be read.

        Returns
        -------
        None.

        """

        """."""
        self.sql_connection = filepath
        self.spectrum_column_names = self._get_column_names('Spectrum')

    def parse_file(self, filepath, **kwargs):
        """
        Parse the file's data and metadata into a flat list of dictionaries.


        Parameters
        ----------
        filename : str
            Filepath of the SLE file to be read.

        Returns
        -------
        self.spectra
            Flat list of dictionaries containing one spectrum each.

        """
        if 'average_scans' in kwargs.keys():
            self.average_scans = kwargs['average_scans']
        else:
            self.average_scans = True

        # initiate connection to sql file
        self.initiate_file_connection(filepath)

        # read and parse sle file
        self.set_current_file(filepath)
        self._get_XML_schedule()
        self.spectra = self._flatten_xml(self.xml)
        print(self.spectra)
        self._attach_node_ids()
        self._remove_empty_nodes()
        self._attach_device_protocols()
        self._get_spectrum_metadata_from_sql()
        self._check_encoding()
# =============================================================================
#         self._append_signal_data()
#
#         if len(self.individual_scans) != 0:
#             self._insert_individual_scans()
# =============================================================================
        self._append_scan_data()

        self._convert_to_common_format()
        self._close_con()

        if 'remove_align' in kwargs.keys():
            if kwargs['remove_align']:
                self._remove_fixed_energies()

        if 'remove_syntax' in kwargs.keys():
            if kwargs['remove_syntax']:
                self._remove_syntax()
            else:
                pass
        else:
            self._remove_syntax()

        self._remove_snapshot()
        self._reindex_spectra()
        self._reindex_groups()

        return self.spectra

    def _get_XML_schedule(self):
        """
        Parse the schedule into an XML object.

        Returns
        -------
        None.

        """
        cur = self.con.cursor()
        query = 'SELECT Value FROM Configuration WHERE Key="Schedule"'
        cur.execute(query)
        XML = ET.fromstring(cur.fetchall()[0][0])
        self.xml = XML

    def _append_scan_data(self):
        """
        Get the signal data, convert to counts per seconds and get scan
        metadata (Scan no., loop no. and iteration no.) from each scan and
        attach to each spectrum.

        Returns
        -------
        None.

        """
        self.individual_scans = []
        scan_id = 0
        for idx, spectrum in enumerate(self.spectra):
            # copy node to new instance
            node_id = self._get_sql_node_id(spectrum['spectrum_id'])
            n_channels = self._check_energy_channels(node_id)
            raw_ids = self._get_raw_ids(node_id)
            n_scans = len(raw_ids)

            for n in range(n_scans):
                scan = copy(spectrum)
                scan['scan_id'] = scan_id
                # get signal data for each scan
                signal_data = self._get_one_scan(raw_ids[n])
                # average channels if required
                if n_channels > 1:
                    signal_data = self._sum_channels(signal_data, n_channels)
                # convert to counts per second
                signal_data_cps = self._convert_to_counts_per_sec(
                    signal_data,
                    float(scan['dwell_time'])
                )
                # attach data to scan
                scan['y'] = signal_data_cps
                # no_of_scans_avg['scans'] = 1

                # add metadata including scan, loop no and datetime
                scan_metadata = self._get_scan_metadata(raw_ids[n])
                for key in scan_metadata.keys():
                    scan[key] = scan_metadata[key]

                self.individual_scans += [scan]
                scan_id += 1

        # update self.spectra with the scan data
        self.spectra = self.individual_scans

# =============================================================================
#     def _append_signal_data(self):
#         """
#         Get the signal data and attach to each spectrum
#
#         Returns
#         -------
#         None.
#
#         """
#         self.individual_scans = []
#         for idx, spectrum in enumerate(self.spectra):
#             node_id = self._get_sql_node_id(spectrum['spectrum_id'])
#             n_channels = self._check_energy_channels(node_id)
#             raw_ids = self._getRawids(node_id)
#             n_scans = len(raw_ids)
#             if n_scans > 1:
#                 signal_data = []
#                 for raw_id in raw_ids:
#                     signal_data += [self._get_one_scan(raw_id)]
#                 if self.average_scans:
#                     signal_data = [float(sum(col)/len(col)) for col in zip(*signal_data)]
#                     if n_channels > 1:
#                         signal_data = self._sum_channels(signal_data,n_channels)
#                     spectrum['y'] = signal_data
#                 else:
#                     for scan in signal_data:
#                         if n_channels > 1:
#                             scan = self._sumChannels(scan,n_channels)
#                             spectrum['y'] = scan
#                             spectrum['scans']=1
#                         else:
#                             spectrum['y'] = scan
#                             spectrum['scans']=1
#                         self.individual_scans += [[copy(spectrum),idx]]
#             else:
#                 signal_data = self._get_one_scan(raw_ids[0])
#                 if n_channels > 1:
#                     signal_data = self._sum_channels(signal_data,n_channels)
#                 spectrum['y'] = signal_data
#
#     def _insert_individual_scans(self):
#         """
#         Insert individual scans in the order they were measured.
#
#         The number of items in self.spectra is first determined from the
#         number of spectrum nodes in the XML file. The number of spectrum
#         nodes is not necessarily the same as the number of spectra in the
#         sle file. If individual scans were saved separately, then each
#         spectrum node might have multiple scans. If 'average_scans' was not
#         chosen to be true in the converter, then the user wants to keep each
#         individual scan. In this case, we need to duplcate the metadata for
#         each scan and append the individual scans at the correct indices
#         of the self.spectra list.
#
#         Returns
#         -------
#         None.
#
#         """
#         ids = list(set([i[1] for i in self.individual_scans]))
#         for idx in reversed(ids):
#             spectra = [i[0] for i in self.individual_scans if i[1] == idx]
#             for spectrum in reversed(spectra):
#                 spectrum = copy(spectrum)
#                 spectrum['scans'] = 1
#                 insert_idx = idx+1
#                 self.spectra.insert(insert_idx, spectrum)
#             self.spectra.pop(idx)
# =============================================================================

    def _check_energy_channels(self, node_id):
        """
        Get the number of separate energy channels for the spectrum.

        This checks to see if the spectrum was saved with separated energy
        channels.

        Parameters
        ----------
        node_id : int
            Internal node ID of spectrum in SLE sql database.

        Returns
        -------
        n_channels : int
            Number of separate energy channels for the spectrum at node ID.
        """
        cur = self.con.cursor()
        query = 'SELECT EnergyChns FROM Spectrum WHERE Node="{}"'.format(
            node_id)
        cur.execute(query)
        result = cur.fetchall()
        if len(result) != 0:
            n_channels = result[0][0]
        return n_channels

    def _get_raw_ids(self, node_id):
        """
        Get the raw IDs from SQL.

        There is one raw_id for each individual scan when scans were not
        already averaged in the sle file.
        To know which rows in the detector data table belong to which scans,
        one needs to first get the raw_id from the RawData table.

        Parameters
        ----------
        node_id : int
            Internal node ID of spectrum in SLE sql database.

        Returns
        -------
        list
            List of raw IDs for the given note ID.

        """
        cur = self.con.cursor()
        query = 'SELECT RawId FROM RawData WHERE Node="{}"'.format(node_id)
        cur.execute(query)
        return [i[0] for i in cur.fetchall()]

    def _check_number_of_scans(self, node_id):
        """
        Get the number of separate scans for the spectrum.

        Parameters
        ----------
        node_id : int
            Internal node ID of spectrum in SLE sql database.

        Returns
        -------
        int
            Number of separate scans for the spectrum.

        """
        cur = self.con.cursor()
        query = 'SELECT RawId FROM RawData WHERE Node="{}"'.format(node_id)
        cur.execute(query)
        return len(cur.fetchall())

    def _get_detector_data(self, node_id):
        """
        Get the detector data from sle file.

        The detector data is stored in the SQLite database as a blob.
        To know which blobs belong to which scans, one needs to first get the
        raw_id from the RawData table.

        Parameters
        ----------
        node_id : int
            Internal node ID of spectrum in SLE sql database.

        Returns
        -------
        detector_data : list
            List of lists with measured data.

        """
        cur = self.con.cursor()
        query = 'SELECT RawID FROM RawData WHERE Node="{}"'.format(node_id)
        cur.execute(query)
        raw_ids = [i[0] for i in cur.fetchall()]
        detector_data = []
        if len(raw_ids) > 1:
            for raw_id in raw_ids:
                detector_data += [self._get_one_scan(raw_id)]
        else:
            raw_id = raw_ids[0]
            detector_data = self._get_one_scan(raw_id)

        return detector_data

    def _attach_device_protocols(self):
        """
        Get the device protocol for each node and add the paramaters of
        thePhoibos to the spectra table. Occassionally these are not
        recorded, if this is the case just skip the group.

        Returns
        -------
        None.

        """
        # iterate through each spectrum
        for spectrum in self.spectra:
            # conver the xml xps id to the node ID and get the device protocol
            cur = self.con.cursor()
            protocol_node_id = self._get_sql_node_id(
                spectrum['device_group_id'])
            query = 'SELECT Protocol FROM DeviceProtocol WHERE Node="{}"'.format(
                protocol_node_id)
            result = cur.execute(query).fetchone()

            # if a record was accessed then parse, if not skip
            if result:
                protocol = ET.fromstring(result[0])

                # parse protocol
                for device in protocol.iter('Command'):
                    # we just want to get the settings for the phoibos for now:
                    if 'Phoibos' in device.attrib['UniqueDeviceName']:
                        # iterate through the parameters and add to spectrum
                        # dict
                        for parameter in device.iter('Parameter'):
                            spectrum[parameter.attrib['name']] = parameter.text

    def _get_one_scan(self, raw_id):
        """
        Get the detector data for a single scan and convert it to float.

        The detector data is stored in the SQLite database as a blob.
        This function decodes the blob into python float. The blob can be
        enoded as float or double in the SQLite table.

        Parameters
        ----------
        raw_id : int
            Raw ID of the single scan.

        Returns
        -------
        stream : list
            List with measured data.

        """
        cur = self.con.cursor()
        query = 'SELECT Data, ChunkSize FROM CountRateData WHERE RawId="{}"'.format(
            raw_id)
        cur.execute(query)
        results = cur.fetchall()
        buffer = self.encoding[1]
        encoding = self.encoding[0]
        stream = []
        for result in results:
            length = result[1] * buffer
            data = result[0]
            for i in range(0, length, buffer):
                stream.append(struct.unpack(encoding, data[i:i + buffer])[0])
        return stream

    def _parse_external_channels(self, channel):
        """
        Parse additional external channels.

        Parameters
        ----------
        channel : int
            DESCRIPTION.

        Returns
        -------
        None.

        """
        """"""
        if len(channel) != 0:
            pass

    def _get_spectrum_metadata_from_sql(self):
        """
        Get the metadata stored in the SQLite Spectrum table

        Returns
        -------
        None.

        """
        for spectrum in self.spectra:
            node_id = self._get_sql_node_id(spectrum['spectrum_id'])
            cur = self.con.cursor()
            query = 'SELECT * FROM Spectrum WHERE Node="{}"'.format(node_id)
            cur.execute(query)
            results = cur.fetchall()
            if len(results) != 0:
                results = results[0]

            column_names = self.spectrum_column_names
            combined = {
                k: v for k, v in dict(zip(column_names, results)).items()
                if k in self.sql_metadata_map.keys()}
            combined = copy(combined)
            if 'EnergyType' not in combined.keys():
                combined['EnergyType'] = 'Binding'
            for k, v in combined.items():
                spectrum[k] = v

            query = 'SELECT Data FROM NodeData WHERE Node="{}"'.format(node_id)
            cur.execute(query)
            results = ET.fromstring(cur.fetchall()[0][0])
            for i in results.iter('AnalyzerSpectrumParameters'):
                spectrum['workfunction'] = i.attrib['Workfunction']
                spectrum['step_size'] = float(i.attrib['ScanDelta'])

    def _get_scan_metadata(self, raw_id):
        """
        Get the scan and the loop/iteration number of each spectrum scan
        and the datetime it was taken from the RawData table.

        Parameters
        ----------
        raw_id : int
            raw id of the scan in the RawData table.

        Returns
        -------
        scan_meta : dict
            dictionary containing scan metadata.

        """
        # get string Trace from RawData
        # self.con = sqlite3.connect(self.sql_connection)
        cur = self.con.cursor()
        query = 'SELECT ScanDate, Trace  FROM RawData WHERE RawID="{}"'.format(
            raw_id)
        result = cur.execute(query).fetchone()
        # process metadata into a dictionary
        scan_meta = {}
        scan_meta['time_stamp_trace'] = result[0]
        scan_meta.update(self._process_trace(result[1]))

        return scan_meta

    def _process_trace(self, trace):
        """
        Parse Trace string to determine the Scan, loop and iteration for the
        given trace.

        Parameters
        ----------
        trace : str
            string to be parsed.

        Returns
        -------
        trace_dict : dict
            dictionary containing scan loop and iteration params
        """
        trace_dict = {}
        loop = re.findall(r'Loop=([0-9]+)u', trace)
        if len(loop) != 0:
            trace_dict['loop_no'] = loop[0]

        scan = re.findall(r'Scan [\[Idx\] ]+=([0-9]+)u', trace)
        if len(scan) != 0:
            trace_dict['scan_no'] = scan[0]

        ramp = re.findall(r'Ramping Iteration [\[Idx\] ]+=([0-9]+)u', trace)
        if len(ramp) != 0:
            trace_dict['iteration_no'] = ramp[0]

        return trace_dict

    def _convert_to_counts_per_sec(self, signal_data, dwell_time):
        """
        Convert signal data given in counts to counts per second.

        Parameters
        ----------
        signal_data : list
            list of floats representing counts.
        dwell_time : float
            value of dwell_time per scan.

        Returns
        -------
        cps : list
            list of values converted to counts per second.

        """
        cps = [n / dwell_time for n in signal_data]
        return cps

    def _get_sql_node_id(self, xml_id):
        """
        Get the SQL internal ID for the NodeID taken from XML.

        Sometimes the NodeID used in XML does not eaxtly map to the IDs for
        Spectra in the SQL tables. To fix this, there is a node mapping.

        Parameters
        ----------
        xml_id : int
            ID in the XML schedule.

        Returns
        -------
        node_id : int
            ID in the SQL tables.

        """
        cur = self.con.cursor()
        query = 'SELECT Node FROM NodeMapping WHERE InternalID="{}"'.format(
            xml_id)
        cur.execute(query)
        node_id = cur.fetchall()[0][0]
        return node_id

    def _attach_node_ids(self):
        """
        Attach the node_id to each spectrum in the spectra list.

        Returns
        -------
        None.

        """
        for spectrum in self.spectra:
            xml_id = spectrum['spectrum_id']
            node_id = self._get_sql_node_id(xml_id)
            spectrum['node_id'] = node_id

    def _remove_empty_nodes(self):
        """
        Remove entries from spectra list that have no spectrum in SQLite.

        Returns
        -------
        None.
        """
        for j in reversed([i for i in enumerate(self.spectra)]):
            idx = j[0]
            spectrum = j[1]
            node_id = spectrum['node_id']
            cur = self.con.cursor()
            query = 'SELECT Node FROM Spectrum WHERE Node="{}"'.format(node_id)
            cur.execute(query)
            result = cur.fetchall()
            if len(result) == 0:
                del self.spectra[idx]

    def _get_energy_data(self, spectrum):
        """
        Create an array of x values.

        Parameters
        ----------
        spectrum : dict
            Dictionary with spectrum data and metadata.

        Returns
        -------
        x : list
            List of uniformly separated energy values.

        """
        if spectrum['x_units'] == 'binding energy':
            start = spectrum['start_energy']
            step = spectrum['step_size']
            points = spectrum['n_values']
            x = [start - i * step for i in range(points)]
        elif spectrum['x_units'] == 'kinetic energy':
            start = spectrum['start_energy']
            step = spectrum['step_size']
            points = spectrum['n_values']
            x = [start + i * step for i in range(points)]
        return x

    def _get_table_names(self):
        """
        Get a list of table names in the current database file.

        Returns
        -------
        data : list
            List of spectrum names.

        """
        """."""
        cur = self.con.cursor()
        cur.execute('SELECT name FROM sqlite_master WHERE type= "table"')
        data = [i[0] for i in cur.fetchall()]
        return data

    def _get_column_names(self, table_name):
        """
        Get the names of the columns in the table.

        Parameters
        ----------
        table_name : str
            Name of SQL table.

        Returns
        -------
        names : list
            List of descriptions.

        """
        cur = self.con.cursor()
        cur.execute(('SELECT * FROM {}').format(table_name))
        names = [description[0] for description in cur.description]
        return names

    def _close_con(self):
        """
        Close the database connection.

        Returns
        -------
        None.

        """
        self.con.close()

    def _convert_date_time(self, timestamp):
        """
        Convert the native time format to the one we decide to use.

        Parameters
        ----------
        timestamp : str
            Native time format of SLE files.

        Returns
        -------
        date_time : str
            Datetime string in the format '%Y-%b-%d %H:%M:%S.%f'.

        """
        date_time = datetime.strptime(timestamp, '%Y-%b-%d %H:%M:%S.%f')
        date_time = datetime.strftime(date_time, '%Y-%m-%d %H:%M:%S.%f')
        return date_time

    def _re_map_keys(self, dictionary, key_map):
        """
        Map the keys returned from the SQL table to the preferred keys for
        the parser output.

        Parameters
        ----------
        dictionary : dict
            Dictionary with data and metadata for a spectrum.
        key_map : TYPE
            DESCRIPTION.

        Returns
        -------
        dictionary : dict
            Dictionary with data and metadata for a spectrum with new keys.

        """
        keys = [k for k in key_map.keys()]
        for k in keys:
            if k in dictionary.keys():
                dictionary[key_map[k]] = dictionary.pop(k)
        return dictionary

    def _drop_unused_keys(self, dictionary, keys_to_drop):
        """
        Remove any keys parsed from sle that are not needed

        Parameters
        ----------
        dictionary : dict
            Dictionary with data and metadata for a spectrum.
        keys_to_drop : list
            List of metadata keys that are not needed.

        Returns
        -------
        None.

        """
        for key in keys_to_drop:
            if key in dictionary.keys():
                dictionary.pop(key)

    def _change_energy_type(self, energy):
        """
        Change the strings for energy type to the preferred format.

        Parameters
        ----------
        energy : str
            'Binding' or 'Kinetic'

        Returns
        -------
        str
            'binding energy' or 'kinetic energy'

        """
        if energy == 'Binding':
            return 'binding energy'
        elif energy == 'Kinetic':
            return 'kinetic energy'

    def _re_map_values(self, dictionary):
        """
        Map the values returned from the SQL table to the preferred format.

        Parameters
        ----------
        dictionary : dict
            Dictionary with data and metadata for a spectrum.

        Returns
        -------
        dictionary : dict
            Dictionary with data and metadata for a spectrum with
            preferred keys for values.

        """
        for k, v in self.value_map.items():
            dictionary[k] = v(dictionary[k])
        return dictionary

    def _sum_channels(self, data, n):
        """
        Sum together energy channels.

        Parameters
        ----------
        data : list
            Array of measured daata .
        n : int
            Number of channels to be summed.

        Returns
        -------
        list
            Summed data across n_channels.

        """

        n_points = int(len(data) / n)
        summed = np.sum(np.reshape(np.array(data), (n_points, n)), axis=1)
        return summed.tolist()

    def _check_encoding(self):
        """
        Check whether the binary data should be decoded float or double.

        Returns
        -------
        None.

        """
        cur = self.con.cursor()
        query = 'SELECT LENGTH(Data),ChunkSize FROM CountRateData LIMIT 1'
        cur.execute(query)
        result = cur.fetchall()[0]
        chunksize = result[1]
        data = result[0]

        if data / chunksize == 4:
            self.encoding = self.encodings_map['float']
        elif data / chunksize == 8:
            self.encoding = self.encodings_map['double']
        else:
            print('This binary encoding is not supported.')

    def _flatten_xml(self, xml):
        """
        Flatten the nested XML structure, keeping only the needed metadata.

        This method has to be implemented in the inherited parsers.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            XML schedule of the experiment.

        Returns
        -------
        collect : list
            List of dictionary with spectra metadata.

        """
        pass

    def _reindex_spectra(self):
        """
        Re-number the spectrum_id.

        Returns
        -------
        None.

        """
        for idx, spectrum in enumerate(self.spectra):
            spectrum['spectrum_id'] = idx

    def _reindex_groups(self):
        """
        Re-number the group_id.

        Returns
        -------
        None.

        """
        group_ids = list(set([spec['group_id'] for spec in self.spectra]))
        for idx, group_id in enumerate(group_ids):
            for spec in self.spectra:
                if int(spec['group_id']) == int(group_id):
                    spec['group_id'] = copy(idx)

    def _convert_to_common_format(self):
        """
        Reformat spectra into the format needed for the Converter object

        Returns
        -------
        None.

        """
        maps = {}
        for m in self.key_maps:
            maps.update(m)
        for spec in self.spectra:
            self._re_map_keys(spec, maps)
            self._re_map_values(spec)
            self._drop_unused_keys(spec, self.keys_to_drop)
            spec['data'] = {}
            spec['data']['x'] = self._get_energy_data(spec)
            spec['data']['y'] = spec.pop('y')
            spec['y_units'] = 'Counts per Second'

    def _remove_fixed_energies(self):
        """
        Remove spectra measured with the scan mode FixedEnergies.

        Returns
        -------
        None.

        """
        self.spectra = [spec for spec in self.spectra
                        if spec['scan_mode'] != 'FixedEnergies']

    def _remove_syntax(self):
        """
        Remove the extra syntax in the group name.

        Returns
        -------
        None.

        """
        for spectrum in self.spectra:
            new_name = spectrum['group_name'].split('#', 1)[0]
            new_name = new_name.rstrip(', ')
            spectrum['group_name'] = new_name

    def _remove_snapshot(self):
        """
        Remove spectra required in Snapshot mode.

        Returns
        -------
        None.

        """
        self.spectra = [spec for spec in self.spectra
                        if 'Snapshot' not in spec['scan_mode']]

    def get_sle_version(self):
        """
        Get the Prodigy SLE version from the file.

        Returns
        -------
        version : TYPE
            DESCRIPTION.

        """
        cur = self.con.cursor()
        query = 'SELECT Value FROM Configuration WHERE Key=="Version"'
        cur.execute(query)
        version = cur.fetchall()[0][0]
        return version


class SleParserV1(SleParser):
    supported_versions = ['1.2', '1.8', '1.9', '1.10', '1.11', '1.12', '1.13']

    def _flatten_xml(self, xml):
        """
        Flatten the nested XML structure, keeping only the needed metadata.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            XML schedule of the experiment.

        Returns
        -------
        collect : list
            List of dictionary with spectra metadata.

        """
        collect = []
        for measurement_type in self.measurement_types:
            for group in xml.iter(measurement_type):
                data = {}
                data['analysis_method'] = measurement_type
                data['devices'] = []

                for j in group.iter('DeviceCommand'):
                    settings = {}
                    for k in j.iter('Parameter'):
                        settings[k.attrib['name']] = k.text
                        data.update(copy(settings))

                    data['devices'] += [j.attrib['DeviceType']]

                    # data['devices'] += [{'device_type' : j.attrib['DeviceType'],
                    #                     'settings':settings}]
                for spectrum_group in group.iter('SpectrumGroup'):
                    data['group_name'] = spectrum_group.attrib['Name']
                    data['group_id'] = spectrum_group.attrib['ID']
                    settings = {}
                    for comm_settings in spectrum_group.iter(
                            'CommonSpectrumSettings'):
                        for setting in comm_settings.iter():
                            if setting.tag == 'ScanMode':
                                settings[setting.tag] = setting.attrib['Name']
                            elif setting.tag == 'SlitInfo':
                                for key, val in setting.attrib.items():
                                    settings[key] = val
                            elif setting.tag == 'Lens':
                                settings.update(setting.attrib)
                            elif setting.tag == 'EnergyChannelCalibration':
                                settings['calibration_file'] = setting.attrib['File']
                            elif setting.tag == 'Transmission':
                                settings['transmission_function'] = setting.attrib['File']
                            elif setting.tag == 'Iris':
                                settings['iris_diameter'] = setting.attrib['Diameter']
                    data.update(copy(settings))

                    for spectrum in spectrum_group.iter('Spectrum'):
                        data['spectrum_id'] = spectrum.attrib['ID']
                        data['spectrum_type'] = spectrum.attrib['Name']
                        settings = {}
                        for setting in spectrum.iter('FixedEnergiesSettings'):
                            settings['dwell_time'] = float(
                                setting.attrib['DwellTime'])
                            settings['start_energy'] = float(
                                copy(setting.attrib['Ebin']))
                            settings['pass_energy'] = float(
                                setting.attrib['Epass'])
                            settings['lens_mode'] = setting.attrib['LensMode']
                            settings['scans'] = int(setting.attrib['NumScans'])
                            settings['n_values'] = int(
                                setting.attrib['NumValues'])
                            settings['end_energy'] = float(
                                setting.attrib['End'])
                            settings['scans'] = int(setting.attrib['NumScans'])
                            settings['excitation_energy'] = float(
                                setting.attrib['Eexc'])
                            settings['step_size'] = ((
                                settings['start_energy']
                                - settings['end_energy'])
                                / (settings['n_values'] - 1))
                        for setting in spectrum.iter(
                                'FixedAnalyzerTransmissionSettings'):
                            settings['dwell_time'] = float(
                                setting.attrib['DwellTime'])
                            settings['start_energy'] = float(
                                copy(setting.attrib['Ebin']))
                            settings['pass_energy'] = float(
                                setting.attrib['Epass'])
                            settings['lens_mode'] = setting.attrib['LensMode']
                            settings['scans'] = int(setting.attrib['NumScans'])
                            settings['n_values'] = int(
                                setting.attrib['NumValues'])
                            settings['end_energy'] = float(
                                setting.attrib['End'])
                            settings['scans'] = int(setting.attrib['NumScans'])
                            settings['excitation_energy'] = float(
                                setting.attrib['Eexc'])
                            settings['step_size'] = ((
                                settings['start_energy']
                                - settings['end_energy'])
                                / (settings['n_values'] - 1))
                        data.update(copy(settings))
                        collect += [copy(data)]
        return collect


class SleParserV4(SleParser):
    supported_versions = [
        '4.63',
        '4.64',
        '4.65',
        '4.66',
        '4.67',
        '4.68',
        '4.69',
        '4.70',
        '4.71',
        '4.72',
        '4.73'
    ]

    def _flatten_xml(self, xml):
        """
        Flatten the nested XML structure, keeping only the needed metadata.

        Parameters
        ----------
        xml : xml.etree.ElementTree
            XML schedule of the experiment.

        Returns
        -------
        collect : list
            List of dictionary with spectra metadata.

        """
        collect = []
        for measurement_type in self.measurement_types:
            for group in xml.iter(measurement_type):
                data = {}
                data['analysis_method'] = measurement_type
                data['devices'] = []
                data['device_group_id'] = group.attrib['ID']

                for device in group.iter('DeviceCommand'):
                    settings = {}
                    for param in device.iter('Parameter'):
                        settings[param.attrib['name']] = param.text
                        data.update(copy(settings))

                    data['devices'] += [device.attrib['DeviceType']]

                    # data['devices'] += [{'device_type' : j.attrib['DeviceType'],
                    #                     'settings':settings}]
                for spectrum_group in group.iter('SpectrumGroup'):
                    data['group_name'] = spectrum_group.attrib['Name']
                    data['group_id'] = spectrum_group.attrib['ID']
                    settings = {}
                    for comm_settings in spectrum_group.iter(
                            'CommonSpectrumSettings'):
                        for setting in comm_settings.iter():
                            if setting.tag == 'ScanMode':
                                settings[setting.tag] = setting.attrib['Name']
                            elif setting.tag == 'SlitInfo':
                                for key, val in setting.attrib.items():
                                    settings[key] = val
                            elif setting.tag == 'Lens':
                                settings.update(setting.attrib)
                            elif setting.tag == 'EnergyChannelCalibration':
                                settings['calibration_file'] = setting.attrib['File']
                            elif setting.tag == 'Transmission':
                                settings['transmission_function'] = setting.attrib['File']
                            elif setting.tag == 'Iris':
                                settings['iris_diameter'] = setting.attrib['Diameter']
                    data.update(copy(settings))

                    for spectrum in spectrum_group.iter('Spectrum'):
                        data['spectrum_id'] = spectrum.attrib['ID']
                        data['spectrum_type'] = spectrum.attrib['Name']
                        for comment in spectrum.iter('Comment'):
                            data['spectrum_comment'] = comment.text
                        """parameter3 = ET.SubElement(entry, 'Parameter')
                        parameter3.attrib['name'] = 'Coil Current [mA]'
                        parameter3.attrib['type'] = 'double'
                        parameter3.text = str(settings_dict['coil_current'])"""

                        settings = {}
                        for setting in spectrum.iter('FixedEnergiesSettings'):
                            settings['dwell_time'] = setting.attrib['DwellTime']
                            settings['start_energy'] = copy(
                                setting.attrib['Ebin'])
                            settings['pass_energy'] = setting.attrib['Epass']
                            settings['lens_mode'] = setting.attrib['LensMode']
                            settings['scans'] = setting.attrib['NumScans']
                            settings['n_values'] = setting.attrib['NumValues']
                        for setting in spectrum.iter(
                                'FixedAnalyzerTransmissionSettings'):
                            settings['dwell_time'] = setting.attrib['DwellTime']
                            settings['start_energy'] = copy(
                                setting.attrib['Ebin'])
                            settings['pass_energy'] = setting.attrib['Epass']
                            settings['lens_mode'] = setting.attrib['LensMode']
                            settings['scans'] = setting.attrib['NumScans']
                            settings['n_values'] = setting.attrib['NumValues']

                        data.update(copy(settings))

                        collect += [copy(data)]
        return collect
