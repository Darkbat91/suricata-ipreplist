# Suricata IP Reputation list
This is a simple python3 script that pulls reputation from badips.com into a suricata compatible replutation list

## Intent
This can be ran from a local Suricata instance or the files can just be pulled from the github raw page. I intend on utilizing this for some of my production environments so the files should get updated regularly until i schedule a nightly job  to push the updated script output.

### Commands

```
# Ensure directory exists
mkdir /etc/suricata/iprep

# Gather category list
wget https://raw.githubusercontent.com/Darkbat91/suricata-ipreplist/master/categorylist.txt -O /etc/suricata/iprep/categories.txt

# Gather the IP list
wget https://raw.githubusercontent.com/Darkbat91/suricata-ipreplist/master/iplist.txt -O /etc/suricata/iprep/reputation.list

# make sure they are owned by Suricata
chown suricata: -R /etc/suricata/iprep

```



## uncomment the relevant lines in the suricata.yaml

```
# IP Reputation
reputation-categories-file: /etc/suricata/iprep/categories.txt
default-reputation-path: /etc/suricata/iprep
reputation-files:
 - reputation.list
 ```

## Known Limitations

This Project can not pull more than 60 categories due to a maximum count in Suricata. To work around this The script is compressing 61+ into the same category as 60. That is not an ideal solution but having all of the ip addresses is deemed more important than ensuring that all of them are categorized properly. 