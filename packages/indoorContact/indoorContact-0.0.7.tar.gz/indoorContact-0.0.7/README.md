# indoorCont
ABM simulation for indoor contact


## License
indoorContact / version 0.0.7
- install:

```python
!pip install indoorContact
```

## Usage (Run simulation and export movie clip)

### 1. add space from data or make space

``` python
import indoorContact as ic


# -- with data --
# with entrance
space, FDD = ic.makeSpace(DFMap= ic.space_no_ent, FDD = True) #entrance = 2, obstacles = 1

# without entrance
space, entrance, FDD = ic.makeSpace(DFMap= ic.space_ent, FDD = True)

# -- without data --
# no obstacles
space = ic.makeSpace(space_x = 10, space_y = 10)

# deploy obstacles
space, obstacles_loc = ic.makeSpace(space_x = 10, space_y = 10, obstacles= 10)

# with chair
space, obstacles_loc = ic.makeSpace(space_x = 10, space_y = 10, obstacles = 10, chairs = 5)

# with entrance
space, entrance, FDD, obstacles_loc = ic.makeSpace(space_x= 15, space_y = 10, obstacles= 10, FDD = True, entrance = {'x': [15,15], 'y': [0,3]}) #x [from: to] / y: [from: to]

print(space)
```

![space](/indoorContact/screenshot/space.png)

This space is made of 0 and 1. 1 is obstacle (2: chair, 3: wall)




### 2. run contact simulation and count contact

``` python

# no scenario
result_df = ic.contact_Simulation(speed = [0.75, 1.8], activity = 5, totalPop = 10, space = space, entrance = entrance, total_time =100)
result_df = ic.countContact(result_df)

# adding chair scenario
space, obstacles_loc = ic.makeSpace(space_x = 10, space_y = 10, obstacles = 10, chairs = 5)
result_df = ic.contact_Simulation(speed = [0.75, 1.8], activity = 5, chair_scenario = [3, 10, 20], totalPop = 10, space = space, entrance = entrance, total_time =100)

# adding group scenario
space, obstacles_loc = ic.makeSpace(space_x = 10, space_y = 10, obstacles= 10)
result_df = ic.contact_Simulation(speed = [0.75, 1.8], activity = 5, group_scenario = [0.5, [2,3], [50, 10]], totalPop = 15, space = space, total_time =100)

```


![df result](/indoorContact/screenshot/result_df.head().png)

result dataframe of simulation. 
- time: total simulation time
- ID: unique ID of agent
- Sec: each second that each agent stay for
- X, Y: coordinates of agents
- Contact_count: the number of contact
- Vertex: verteces of trajectories
- Speed: speed of agents
- sit: sit or not (chair scenario)
- exit: 1 once agent go out
- STUCK: if agent is stuck and lose the way
- totalP: total population
- Chair: chair location where the agent sit
- group: group (1) or not (0)
- groupedP: population who are in the same group
- Contact_Sec: duration (second) of contact
- Contact_IDs: ID who encounter
- Contact_Pop: population that the agent encounter (physically contact)


### 3. export movie clip of simulation

``` python

# movie clip
ic.simul_clip_export('C:/Users/', result_df, space, 'result_clip.mp4')

```

![screenshot](/indoorContact/screenshot/contact_exper.png)

movie clip:
![movie clip of ABM simulation](/indoorContact/screenshot/contact_exper.mp4)


---

## Related Document: 
 will be added

## Author

- **Author:** Moongi Choi
- **Email:** u1316663@utah.edu
