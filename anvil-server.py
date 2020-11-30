import anvil.server
import pandas as pd
import anvil.media

anvil.server.connect("43NWTP3ICWI4MGJVKVM3TFZP-IWPMKBJPA4RUKN4I")

@anvil.server.callable
def say_hello(name):
  print("Hello from the uplink, %s!" % name)

@anvil.server.callable
def store_data(file):
  with anvil.media.TempFile(file) as file_name:
    if file.content_type == 'text/csv':
      df = pd.read_csv(file_name)
    else:
      df = pd.read_excel(file_name)
    for d in df.to_dict(orient="records"):
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
      app_tables.PF.add_row(**d)
anvil.server.wait_forever()
