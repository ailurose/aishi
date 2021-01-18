[![Foo](https://user-images.githubusercontent.com/67992204/103492314-01a8cd00-4df8-11eb-81e4-5e0d6358e108.png)](https://github.com/ailurose/aishi)


Aishi comes with the following commands and respective help commands to assist in its usage:

**Categories**: [Genshin Impact](https://ailurose.github.io/aishi/commands#genshin-impact) | [Granblue Fantasy](https://ailurose.github.io/aishi/commands#granblue-fantasy) | [League](https://ailurose.github.io/aishi/commands#league) | [Profile](https://ailurose.github.io/aishi/commands#profile) | [Miscellaneous](https://ailurose.github.io/aishi/commands#miscellaneous)

&nbsp;
&nbsp;


## **Genshin Impact**
### Commands

|Command                                                    |Description                                          |Usages|
|---|:---:|:---|
|[`~craft`](https://ailurose.github.io/aishi/commands#craft)|performs material calculations|`~craft [blue/purple/gold] [green amount] [blue amount] [purple amount]`|

#### `~craft`
When `~craft` is called, the bot performs calculations to determine the amount of the specified material you want, based on the amount of materials you stated. The material calculates based on the background colors of each material, aka the item rarity.
##### Example 1: `~craft blue 6` will print that you can make a total of 2 blue materials
##### Example 2: `~craft gold 2 3` will print that you can make a total of 0 gold materials
##### Example 3: `~craft purple 0 14 9` will print that you can make a total of 13 purple materials


&nbsp;
## **Granblue Fantasy**
### Commands

|Command                                                                 |Description                                                                    |Usages            |
|---|:---:|:---|
|[`~raid`](https://ailurose.github.io/aishi/commands#raid)               |sends the GBF raid tweet from specified twitter user                           |`~raid [user]`    |
|[`~@gbfroles`](https://ailurose.github.io/aishi/commands#gbfroles)      |lists the created roles for raids and allows server members to join by reacting|`~@gbfroles`      |

### **Admin Commands**

|Admin Command  |Description                                                                    |Usages            |
|---|:---:|:---|
|[`~@makeroles`](https://ailurose.github.io/aishi/commands#makeroles)    |creates all roles for raids to be reacted when `~@gbfroles` is called          |`~@makeroles`     |
|[`~@addrole`](https://ailurose.github.io/aishi/commands#addrole)        |allows for the creation of individual roles to be added for raids              |`~@addrole [role]`|
|[`~@deleteroles`](https://ailurose.github.io/aishi/commands#deleteroles)|allows for the deletion of individual roles associated to raids                |`~deleteroles`    |

#### `~raid`
When `~raid` is called, the bot will send a message in the channel that includes the most recent tweet by the specified twitter username as well as a separate message including only the raid code for ease of copying.

#### `~gbfroles`
`~gbfroles` sends a message listing all the created roles for the raids and the corresponding raids to each role and allows each server member to join those roles by reacting to the corresponding emotes. Only the administrator can call this command. `~@makeroles` **must** be called before `~gbfroles` or else the server members will be unable to join the roles. See [`~makeroles`](https://ailurose.github.io/aishi/commands#makeroles) for the table listing all the roles and corresponding raids.

#### `~@makeroles`
Calling `~@makeroles` creates the set of roles recommended by Aishi for raids. In order to call for this command, the user must be the administrator. See table below for the roles created via this command and the corresponding raids it represents:

|Role           |Raids                                                                                                          |
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


&nbsp;
## **League**
### Commands

|Command                                                  |Description                                                    |Usages                 |
|---|:---:|:---|
|[`~ammr`](https://ailurose.github.io/aishi/commands#ammr)|lists summoner ARAM MMR                                        |`~ammr [user] [region]`|
|[`~aram`](https://ailurose.github.io/aishi/commands#aram)|lists ARAM MMR of each summoner in game with specified summoner|`~aram [user]`         |

#### `~ammr`
When `~ammr` is called by the server member, the bot will return the ARAM MMR of the specified summoner. Regions include na = North America, euw = EU West, eune = EU Nordic & East. Note that the default region is na.

#### `~aram`
When `~aram` is called by the server member, the bot will return the ARAM MMR of each summoner that is in game with the specified summoner. At the momment, this command only supports na region.


&nbsp;
## **Profile**
### Commands

|Command                                                |Description                                                                           |Usages                          |
|---|:---:|:---|
|[`~pfp`](https://ailurose.github.io/aishi/commands#pfp)|provides the profile of the user with any information that have been added by the user|`~pfp`, `~pfp [user]`, [`~pfp add [title] [description]`](https://ailurose.github.io/aishi/commands#pfp-add), [`~pfp delete [title]`](https://ailurose.github.io/aishi/commands#pfp-delete), [`~pfp deleteall`](https://ailurose.github.io/aishi/commands#pfp-deleteall)|

#### `~pfp`
`~pfp` provides the custom profile of the user. When only `~pfp` is called, it returns the profile of the server member who called the command. Otherwise, if `~pfp [user]` is called, the profile of the mentioned server member will be returned.
##### `~pfp add`
Users may customize their profile by adding information to their profile with a title and description.
###### Example 1: `~pfp add title description` inserts the title as "title" and the description as "description"
###### Example 2: `~pfp add "a long title" "a very long description"` inserts the title as "a long title" and the description as "a very long description"
##### `~pfp delete`
Users may customize their profile by deleting specified information that was previously added into their profile
###### Example 1: `~pfp delete title` will delete the title named "title" and its corresponding description from the user's profile
###### Example 2: `~pfp delete "a very long title"` will delete the title named "a very long title" and its corresponding description from the user's profile
##### `~pfp deleteall`
If users do not wish to have any of the customizations added to their profile anymore, the user may delete their customizations by calling this command.


&nbsp;
## **Miscellaneous**
### Commands

|Command                                                  |Description                            |Usages|
|---|:---:|:---|
|[`~flip`](https://ailurose.github.io/aishi/commands#flip)|flips a coin and returns heads or tails|`~flip`|

#### `~flip`
`~flip` allows the user to flip a coin and will return heads or tails



[Back to home page](https://ailurose.github.io/aishi/)
