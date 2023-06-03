<p align="center"> <img src="./etc/metamorf-logo.png" width="500" /> </p>


## What is Metamorf

Metamorf is a Metadata Suite that generates SQL code within a framework based on *select* statements.
Those queries are generated based on metadata that the user has entered on the framework.
All this metadata needs to be processed to maximize its potential. Metamorf can execute and materialize
these datasets, control the lineage end to end, even deploy an api sharing all the metadata.

## Architecture

<p align="center"> <img src="./etc/metamorf-arch.png" width="600" /> </p>

Metamorf is a Python Software that orchestrates, controls and transforms data. From a 
metadata entry, Metamorf process the metadata to full its system and in exchange grants a series
of functionalities that allows to control all your datawarehouse.

Metamorf works with the concept of *owner*: it can be a user or a use case. Some actions of metamorf
can be done selecting an owner, indicated  on the configuration file.
It can be useful for teamwork using the same Metadata Database and isolating each user or use case
under development. Is up to you.

Metamorf stores all the metadata historically, it means that the users can see the status of their
datawarehouse in the past at any time and know how the data was processed.


### Databases

Actually Metamorf supports the following databases:
- Snowflake
- SQLite

## How to Start
To install Metamorf, you need Python 3.10, and you can install it using pip. 
    
    pip install metamorf

Once installed, you can see all the available commands typing:

    metamorf help

For a quick start, create a directory where you want to locate all the configuration files.

    metamorf init

You have initialized your environment to configure Metamorf. The basic configuration is through
a SQLite database.
  
Metamorf can be deployed where the configuration file says. If SQLite is selected (as default)
and it doesn't exist, Metamorf will create the databases. Try it!

    metamorf deploy

Now you have on your repository all the configuration files and a data and metadata example databases.  
To deploy an example on both databases, just type:

    metamorf deploy-example

A fake dataset is deployed on the data database, and a metadata entry is inserted on the metadata database.
You can just watch all these things with any Database Tool as DBeaver.  
  
If you want to process these metadata, try the command:

    metamorf process

Now all the metadata is processed and the main tables of Metamorf are populated.
To see if all works, you can just type any of the features that Metamorf offers:

If you want to run the processes indicated on the metadata, you can just type:

    metadata run

Probably you just want the SQL Files to execute from other platforms, type then:

    metadata output

The results are located on the output folder on your repository.  

The configuration file permits you to configure Metamorf to adapt it to your needs.
For example, one interesting option could be to generate all you datasets on *dbt* format.
To achieve it, just change your *configuration.yml* file, **output** option, **type** value to **dbt**.

      output:
        type: dbt

You can execute again 
    
    metadata output

And now you have all the necessary files for your dbt project.  

This tutorial is just a small demonstration about metamorf and its potential.

*Note: First versions of Metamorf were only tested on Windows OS.*

## Commands

Metamorf works with commands as:

    metamorf [command] [arguments]

It accepts the commands showed in this section. Some of these commands accept arguments 
to select some datasets / files or an owner.

Arguments to specify the file or the target table:

    --select name_of_the_selection
    -s name_of_the_selection

Arguments to specify the owner:

    --owner target_owner_name
    -o target_owner_name

- **help**: it shows all the commands available
- **manifest**: it generates a manifest json file with all the dataset information. It will be used in future features.
- **api**: it deploys an api that serve all the dataset information.
- **validate**: it validates the configuration file.
- **init**: It creates the necessary folders, configuration file and other elements to execute metamorf on the current path. 
The user can specify the target databases type (data and metadata) with the arguments [-d/--database, -m/--metadata]<sup>1</sup> 
- **deploy**: It deploys Metamorf on the metadata database indicated on the configuration file.
- **deploy-example**: It deploys an example on both databases.
- **download**: It downloads all the metadata entry to the entry folder. It can be indicated the owner and the tables.
- **upload**: It uploads the metadata entry from the entry folder to the metadata database.
- **commit**: It commits the metadata entry from the actual owner. It can be useful to save gold versions and develop new datasets without any risk.
- **recover**: It recovers the last commit from the actual owner.
- **output**: It generates all the dataset files on the *output* folder.
- **delete**: It deletes all the metadata from the metadata entry.
- **backup**: It downloads a backup from all the system.
- **restore**: It uploads all the backup to the system.

<sup>1</sup> Actually Metamorf accepts the databases indicated on this [section](#databases)

## Roadmap

- *[Under development]* Include Datavault 2.0 Module to simplify the metadata entry for this modelling.
- *[Under development]* Include a metadata entry validator to avoid unexpected errors.
- *[Near development]* Include File loader.
- *[Near development]* Create a detailed documentation.
- *[Near development]* Include more materialization and more metadata transformation speeders.
- *[Near development]* Include easier metadata entry system.
- *[Near development]* Include some more databases as PostgreSQL and MySQL.
- *[Future development]* Include more databases.
- *[Future development]* Security Framework based on metadata for the datawarehouse

## Contact

Creator: **Guillermo Aumatell Salom**  
Email: **gaumatellsalom@gmail.com**


**Notice: Metamorf is in beta phase.**