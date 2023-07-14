import json, sys, os


class PackageInstaller:
  def __init__(self):
    # Loading packages
    with open("packages.json", "r") as file:
      content = file.read()
      file.close()
    
    try:
      self.packages = json.loads(content)
    except:
      print("unable to parse packages.json")
      exit(0)
    
    # Mapping for choice
    i = 1
    self.mapping = {}
    for package in self.packages.keys():
      self.mapping[str(i)] = package
      i += 1
    self.mapping[str(i)] = "exit"


  def print_available(self):
    print("Verfügbare Pakete:")
    for key, value in self.mapping.items():
      print(key, value)


  def choice_package(self):
    choices = input("Bitte wähle die Pakete die installiert werden sollen(1 | 1, 2 | ...): ")
    choices = choices.replace(" ", "").split(",")
    
    try:
      if int(max(choices)) > len(self.mapping.keys()) or int(min(choices)) <= 0:
        print("Die Auswahl ist ungültig...")
        return
    except:
      print("Die Auswahl ist ungültig...")
      return

    for choice in choices:
      self.install_package(self.mapping.get(choice))


  def install_package(self, package: str):
    if package == "exit":
      exit(0)

    print(f"Installing package {package}...")
    
    target = self.packages.get(package).get(sys.platform)
    
    if sys.platform == "linux":
        target = target.get("arch")

    for x in target:
      status = os.system(x)
      if status != 0:
        print("Installation abord")
        break
    
    print("Remove unneeded files...")

    for file in os.listdir("."):
      if file == ".git":
        continue

      if not os.path.isdir(file):
        continue

      os.system(f"rm -rf {file}")


if __name__ == "__main__":
  packageInstaller = PackageInstaller()
  while True:
    packageInstaller.print_available()
    packageInstaller.choice_package()
