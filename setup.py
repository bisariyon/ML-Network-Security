from setuptools import setup, find_packages

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->list[str]:
    """
    This function will return the list of requirements
    """
    requirements_list: list[str] = []
    try:
        with open(file_path) as file_obj:
            requirement_line = file_obj.readlines()

            for line in requirement_line:
                requirement = line.strip()
                if requirement and requirement!= HYPHEN_E_DOT:
                    requirements_list.append(requirement)

    except FileNotFoundError:
        print(f"Requirements file not found: {file_path}")
        
    return requirements_list

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author="Bisariyon",
    author_email="deepbisariya@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)