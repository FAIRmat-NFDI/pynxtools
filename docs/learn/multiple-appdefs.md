# Multiple Application Definitions in NeXus

!!! danger "Work in progress"

    This part of the documentation is still being written and it might be confusing or incomplete.

This tutorial showcases how to employ multiple application definitions in NeXus for creating a file that conforms to various definitions simultaneously.

!!! info "Prerequisites"

    Familiarity with the basics of NeXus and its application definitions is required. For an introduction to NeXus, please refer to the [basic documentation](nexus-primer.md).

In a laboratory setting, the data we collect can vary significantly depending on the experiment's specific setup. Consider, for instance, an experiment characterized using the `NXexperiment` application definition. Suppose we want to enhance this experiment by incorporating energy resolution details. A straightforward approach might involve creating a specialized sub-application definition, like `NXexperiment_energy_resolved`, to include metadata about the experiment's energy resolution.

While this method is effective for initial expansions of the metadata, it becomes cumbersome when trying to merge multiple enhancements into a single application definition. Imagine we wish to integrate additional elements that provide time resolution data for our experiment. 
We need to create three sub application definitions to reflect all combinations: `NXexperiment_time_resolved`, `NXexperiment_energy_resolved` and `NXexperiment_energy_time_resolved`.
For three experimental facets we already need 7 sub application definitions. An additional problem is that we have to repeat the whole procedure for all experiments we like to add the specific traits to. So if we have three different parent application definitions we already need to create 9 sub application definitions just to add energy and time resolution.

The solution for this problem is to specify multiple application definitions while writing a NeXus file to follow different traits of the experiment. This allows us to simply create `NXtime_resolved` and `NXenergy_resolved` and combine it with any experiment we want to use it with.
This comes, however, with a few drawbacks. One of them is that it is currently not possible to write a file which wants to use two different application definitions which have conflicting fields. While this is generally possible in the framework of NeXus, since every application definition creates their own namespace, this is not supported when the paths are reduced to entry path notation.

ToDo:
- Make an example of NXexperiment, NXtime_resolved and NXenergy_resolved and show how it is combined into the instance path.
- Also show this for a conflict. Compare concept path (no problem) to instance path (colliding).
- Write a part how it is described in the file that it follows two appdefs `/entry/definitions` as array containing both appdefs.
- Explain that this is no problem with the expanded concept path notation but fails when we only use the instance path.
- Explain the reader concept: One reader for one appdef, then pynxtools will figure out how to combine them (this is domain knowledge for the FAIRmat reader -> will be different when a read/write tool is written somewhere else).
