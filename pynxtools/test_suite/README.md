# Generalized Test stuff for pynxtools plugin
This pynxtools sub-package is to be utilized to write automated test for pynxtools plugins without having deep knowledge of the pynxtools internal architecture. The tool mainly supports for generalised test for all the reader plugins disregarding the technical details of file reader and internal desing of the plugin (It is assumed that the plugin has followed the [plugin template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template)).
## Why it is needed
To test plugin integration with the `pynxtools` core system. The integration test comes in two ways.
1. Test the plugin's integration with `pynxtools` from the plugin's ci/cd.
2. Test if plugin has been integrated with pynxtools properly from pynxtools from pynxtools's ci/cd.

**TODO:** Need to be extend after general consensus.