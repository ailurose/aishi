![AishiLogo](https://user-images.githubusercontent.com/67992204/103492314-01a8cd00-4df8-11eb-81e4-5e0d6358e108.png)


Aishi comes with the following commands and respective help commands to assist in its usage:

## **Granblue Fantasy**
### Commands

|Command                                                 |Description                                         |Usages            |
|---|:---:|:---|
|[`~raid`](https://ailurose.github.io/aishi/commands#raid)|sends the GBF raid tweet from specified twitter user|`~raid [user]`    |

#### `~raid`
When `~raid` is called, the bot will send a message in the channel that includes the most recent tweet by the specified twitter username as well as a separate message including only the raid code for ease of copying.

### **Admin Commands**

|Admin Command  |Description                                                                    |Usages            |
|---|:---:|:---|
|[`~@makeroles`](https://ailurose.github.io/aishi/commands#makeroles)    |creates all roles for raids to be reacted when `~@gbfroles` is called          |`~@makeroles`     |
|[`~@addrole`](https://ailurose.github.io/aishi/commands#addrole)        |allows for the creation of individual roles to be added for raids              |`~@addrole [role]`|
|[`~@deleteroles`](https://ailurose.github.io/aishi/commands#deleteroles)|allows for the deletion of individual roles associated to raids                |`~deleteroles`    |
|[`~@gbfroles`](https://ailurose.github.io/aishi/commands#gbfroles)      |lists the created roles for raids and allows server members to join by reacting|`~@gbfroles`      |

#### `~@makeroles`
Calling `~@makeroles` creates the set of roles recommended by Aishi for raids. In order to call for this command, the user must be the administrator. See table below for the roles created via this command and the corresponding raids it represents:
|Role|Raids|
|---|:---|
|M1 raids       |Tiamat Omega, Colossus Omega, Leviathan Omega, Yggdrasil Omega, Luminiera Omega, Celeste Omega                 |
|M2 raids       |Shiva, Europa, Godsworn Alexiel, Grimnir, Metatron, Avatar                                                     |
|T3 raids       |Prometheus, Ca Ong, Gilgamesh, Morrigna, Hector, Anubis                                                        |
|Dragon raids   |Wilnas, Wamdus, Galleon, Ewiyar, Lu Woh, Fediel, Lindwurm                                                      |
|T1&2           |Twin Elements, Macula Marius, Medusa, Nezha, Apollo, Dark Angel Olivia, Athena, Grani, Baal, Garuda, Odin, Lich|
|Disciples raids|Michael, Gabriel, Uriel, Raphael, The Four Primachs                                                            |
|Nightmare raids|Akasha, Tiamat Malice, Leviathan Malice, Phronesis, Grand Order                                                |
|ROTB raids     |Huanglong, Qilin, Huanglong and Qilin                                                                          |
|Baha raids     |Proto Bahamut, Ultimate Bahamut                                                                                |

#### `~@addrole`
If the server would like to create a new role to be added to the list of raids, the administrator may call the command `~@addrole` which will create one single role per command to be added.

#### `~@deleteroles`
If the server wishes to no longer use the created roles for raids, the admin may call the command `~@deleteroles` to delete all raid roles.

#### `~@gbfroles`
`~@gbfroles` sends a message listing all the created roles for the raids and the corresponding raids to each role and allows each server member to join those roles by reacting to the corresponding emotes. `~@makeroles` **must** be called before `~@gbfroles` or else the server members will be unable to join the roles. See [`~makeroles`](https://ailurose.github.io/aishi/commands#makeroles) for the table listing all the roles and corresponding raids.



## **League**
### Commands

|Command|Description                                                    |Usages                 |
|---|:---:|:---|
|`~ammr`|lists summoner ARAM MMR                                        |`~ammr [user] [region]`|
|`~aram`|lists ARAM MMR of each summoner in game with specified summoner|`~aram [user] [region]`|



## **Profile**
### Commands

|Command|Description                                                                          |Usages                                                         |
|---|:---:|:---|
|`~pfp` |provides the profile of the user with any game codes that have been added by the user|`~pfp [add <title> <description> | delete <title> | deleteall]`|
