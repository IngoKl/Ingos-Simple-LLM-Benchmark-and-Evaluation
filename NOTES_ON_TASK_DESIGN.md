# Notes on Task Design

This document contains some notes on task design. They are simple ideas and insights that arose from the process of designing tasks for this project.

Please refer to the ample amount of research on AI benchmarks and evaluation for verified and rigorously tested insights.

* Following an approach where model output is evaluated against a given solution heavily relies on the model's ability to adhere to the specified output format. Therefore, in many cases, this ability is tested alongside the task itself.
* As tasks ideally work for multiple and diverse models, model-specific prompt engineering should be avoided.
