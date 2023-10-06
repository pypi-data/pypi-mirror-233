[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)


# [{model_name}: {model_headline}]({model_url})

{model_description}

This is a derivative of the implementation of {model_name} found [here]({source_repo}).

More details, such as model latency and throughput running on various devices, can be found at {model_url}


## Example & Usage
{package_install_instructions}

Run the demo:
```bash
python -m tetra_model_zoo.{model_id}.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate {model_name} for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate {model_name} for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.{model_id}.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using {model_name} in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of {model_name} can be found [here]({license_url}).


## References
* [{research_paper_title}]({research_paper_url})
* [Source Model Implementation]({source_repo})
