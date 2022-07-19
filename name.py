import csv
import plotly.express as px 

rows = []

with open("name.csv", "r") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        rows.append(row)

headers = rows[0]
planet_data_rows = rows[1:]
#print(headers)
#print(planet_data_rows[0])

headers[0] = "row_num"
solar_system_planet_count = {}

for planet_data in planet_data_rows:
    if solar_system_planet_count.get(planet_data[11]):
        solar_system_planet_count[planet_data[11]]+=1
    else:
        solar_system_planet_count[planet_data[11]]=1

max_solar_system = max(solar_system_planet_count, key = solar_system_planet_count.get)
#print("solar system {} has maximum planets {} out of all the solar systems".format(max_solar_system, solar_system_planet_count[max_solar_system])) 

koi_351_planets = []
for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        koi_351_planets.append(planet_data) 

#print(len(koi_351_planets))
#print(koi_351_planets)

temp_planet_data_rows = list(planet_data_rows)
for planet_data in temp_planet_data_rows:
    planet_mass = planet_data[3]
    if planet_mass.lower() == "unknown":
        planet_data_rows.remove(planet_data)
        continue
    else:
        planet_mass_value = planet_mass.split(" ")[0]
        planet_mass_ref = planet_mass.split(" ")[1]
        if planet_mass_ref == "Jupiters":
            planet_mass_value = float(planet_mass_value)*317.8
        planet_data[3] = planet_mass_value

    planet_radius = planet_data[7]
    if planet_radius.lower() == "unknown":
      planet_data_rows.remove(planet_data)
      continue
    else:
      planet_radius_value = planet_radius.split(" ")[0]
      planet_radius_ref = planet_radius.split(" ")[2]
      if planet_radius_ref == "Jupiter":
          planet_radius_value = float(planet_radius_value)*11.2
      planet_data[7] = planet_radius_value

koi_351_planet_mass = []
koi_351_planet_names = []

for planet_data in koi_351_planets:
    koi_351_planet_mass.append(planet_data[3])
    koi_351_planet_names.append(planet_data[1]) 

koi_351_planet_mass.append(1)
koi_351_planet_names.append("Earth")
#fig = px.bar(x = koi_351_planet_names, y = koi_351_planet_mass)
#fig.show()

temp_planet_data_rows = list(planet_data_rows)

for planet_data in temp_planet_data_rows:
    if planet_data[1].lower() == "hd 100546 b":
        planet_data_rows.remove(planet_data)


planet_masses = []
planet_radiuses = []
planet_names = []

for planet_data in planet_data_rows:
    planet_masses.append(planet_data[3])
    planet_radiuses.append(planet_data[7])
    planet_names.append(planet_data[1])

planet_gravity = []
for index, name in enumerate(planet_names):
  gravity = (float(planet_masses[index])*5.972e+24) / (float(planet_radiuses[index])*float(planet_radiuses[index])*6371000*6371000) * 6.674e-11
  planet_gravity.append(gravity)

#fig = px.scatter(x=planet_radiuses, y=planet_masses, size=planet_gravity, hover_data=[planet_names])
#fig.show()

low_gravity_planets = []
for index, gravity in enumerate(planet_gravity):
    if gravity < 10:
      low_gravity_planets.append(planet_data_rows[index])
#print(len(low_gravity_planets))

planet_type_value = []
for planet_data in planet_data_rows:
  planet_type_value.append(planet_data[6])
#print(list(set(planet_type_value)))

planet_masses = []
planet_radiuses = []
for planet_data in low_gravity_planets:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])
#fig = px.scatter(x = planet_radiuses, y = planet_masses)
#fig.show()

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import seaborn as sns 
X = [] 
for index, planet_mass in enumerate(planet_masses): 
  temp_list = [ planet_radiuses[index], planet_mass ] 
  X.append(temp_list) 
wcss = [] 
for i in range(1, 11): 
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state = 42) 
  kmeans.fit(X) 
  # inertia method returns wcss for that model 
  wcss.append(kmeans.inertia_) 
#plt.figure(figsize=(10,5)) 
#sns.lineplot(range(1, 11), wcss, marker='o', color='red') 
#plt.title('The Elbow Method') 
#plt.xlabel('Number of clusters') 
#plt.ylabel('WCSS') 
#plt.show()

planet_masses = []
planet_radiuses = []
planet_types = []

for planet_data in low_gravity_planets:
  planet_masses.append(planet_data[3])
  planet_radiuses.append(planet_data[7])
  planet_types.append(planet_data[6])

#fig = px.scatter(x = planet_radiuses, y = planet_masses, color = planet_types)
#fig.show()

suitable_planets = []
for planet_data in low_gravity_planets:
  if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
    suitable_planets.append(planet_data)
#print(len(suitable_planets))



#Project 133


temp_suitable_planets = list(suitable_planets) 
orbital_radiuses = [] 
orbital_periods = [] 

for planet_data in suitable_planets:
   orbital_radiuses.append(planet_data[8]) 
   orbital_periods.append(planet_data[9]) 

#fig = px.scatter(x=orbital_radiuses, y=orbital_periods) 
#fig.show()

goldilock_planets = list(suitable_planets)
temp_goldilock_planets = list(suitable_planets)

for planet_data in temp_goldilock_planets:
  if planet_data[8] < 0.38 or planet_data[8] > 2:
    goldilock_planets.remove(planet_data)

#print(len(suitable_planets))
#print(len(goldilock_planets))

planet_speeds = []
for planet_data in suitable_planets:
  distance = 2*3.14*(planet_data[8]*1.496e+9)
  time = planet_data[9]*86400
  speed = distance/time
  planet_speeds.append(speed)

speed_supporting_planets = list(suitable_planets)
temp_speed_supporting_planets = list(suitable_planets)
for index, planet_data in enumerate(temp_speed_supporting_planets):
  if planet_speeds[index] > 200:
    speed_supporting_planets.remove(planet_data)

#print(len(speed_supporting_planets))

#C134

habitable_planets = []
for planet in speed_supporting_planets:
  if planet in goldilock_planets:
    habitable_planets.append(planet)

#print(len(habitable_planets))

final_dict = {}
for index, planet_data in enumerate(planet_data_rows):
  features_list = []
  gravity = (float(planet_data[3])*5.972e+24)/(float(planet_data[7])*float(planet_data[7])*6371000*6371000)*6.674e-11
  try:
    if gravity<100:
      features_list.append("gravity")
  except:
    pass 
  try:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
      features_list.append("planet_type")
  except:
    pass 
  try:
    if planet_data[8] > 0.38 or planet_data[8] < 2:
      features_list.append("goldilock")
  except:
    pass 
  try:
    distance = 2*3.14*(planet_data[8]*1.496e+9)
    time = planet_data[9]*86400
    speed = distance/time
    if speed < 200:
      features_list.append("speed")
  except:
    pass 

  final_dict[index] = features_list

#print(final_dict)