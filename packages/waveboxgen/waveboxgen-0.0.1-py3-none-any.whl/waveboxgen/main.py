import argparse
import os
from .utils import converter
from .templates import Templates

def generate_service(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    basename = converter.to_snake_case(os.path.basename(filepath))

    service_filename = os.path.join(filepath, f"{basename}_service.py")

    if os.path.exists(service_filename):
        index = 1
        while True:
            unique_filename = f"_service_{index}.py"
            service_filename = os.path.join(filepath, f"{basename}{unique_filename}")
            
            if not os.path.exists(service_filename):
                break

            index += 1

    with open(service_filename, 'w') as file:
        file.write(Templates(filepath).service_template())

        print(f"Service generated at {service_filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate a wavebox framework file")
    parser.add_argument('spawn', type=bool, help='Pass this argument to generate file')
    parser.add_argument('service', type=bool, help="Pass this argument to create service file")
    parser.add_argument('filepath', type=str, help='Directory where the service file will be generated')

    args = parser.parse_args()
    if args.spawn is True:
        if args.service is True:
            generate_service(args.filepath)
    