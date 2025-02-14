# Dynamic Pricing Engine for Riding Apps

Dynamic Pricing Engine for Riding Apps is a pricing engine that calculates the price of a ride based on the distance and time taken to complete the ride. The pricing engine uses a base fare, cost per minute, and cost per mile to calculate the price of the ride. The pricing engine also takes into account surge pricing, which increases the price of the ride based on the demand for rides at a particular time.
This is a simple pricing engine that can be used by riding apps to calculate the price of a ride for their customers. The pricing engine is written in Python and can be easily integrated into existing riding apps. The pricing engine is flexible and can be customized to suit the needs of different riding apps.

## Features

- Calculate the price of a ride based on the distance and time taken to complete the ride
- Use a base fare, cost per km to calculate the price of the ride
- Take into account surge pricing to increase the price of the ride based on demand

## Installation

To install the pricing engine, you would need to take actionable steps as below:

- Clone the repository
- Create a virtual environment and Install the dependencies
- Run the tests to validate the installation
- Run the project using the `django`'s `runserver` command

```bash
git clone <repository-url> fincride

cd fincride
python3 -m venv venv

source venv/bin/activate

pip instal poetry
poetry install --no-root

python manage.py test
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

Distributed under the MIT License. See `LICENSE` for more information.
