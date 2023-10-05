# StreamLoom

## Create reusable blocks and weave them into beautiful pipelines.

StreamLoom is a modular and extensible Python framework designed for building, managing, and executing pipelines. With its intuitive block-based structure, users can easily chain tasks and manage data flow, all while seamlessly switching between various executors and transports.

## Features

- **Atomic & Series Data Handling**: StreamLoom can process both singular atomic data and series data streams.

- **Multiple Executors**: Execute blocks using a variety of methods including Process, Async, Threads, Containers, and more.

- **Flexible Transports**: Switch between data transports like sockets, Kafka queues, files, etc., with ease.

- **Extensible & Modular Design**: Easily extend StreamLoom with custom blocks, executors, and transports.

## Installation

Install StreamLoom via pip:

```bash
pip install streamloom
```

## Quick Start

Here's a simple example to get started:

```python
from streamloom import AddBlock, Pipeline, ProcessExecutor, SocketTransport

# Define and connect blocks
add1 = AddBlock(x=10, y=20)
add2 = AddBlock(x=add1.result, y=100)

# Create pipeline with outputs
pipeline = Pipeline(blocks=[add1, add2], outputs={"final_sum": add2.result})

# Execute the pipeline
result = pipeline.execute()
print(result)  # Outputs: {final_sum: 130}
```

For more detailed examples and tutorials, check out our [documentation](documentation_link).

## Documentation

Detailed documentation is available [here](documentation_link).

## Contribution

We welcome contributions to StreamLoom! Please check out our [CONTRIBUTING.md](link_to_contributing_file) for guidelines.

## License

StreamLoom is licensed under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to the community and contributors for their invaluable feedback and contributions.

## Contact

For queries or feedback, please contact [sanygeek@gmail.com](mailto:sanygeek@gmail.com).
