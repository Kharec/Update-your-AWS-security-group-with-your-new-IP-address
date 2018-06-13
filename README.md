# updateRoute53Record

So, this is a simple python script to update your AWS Route53 DNS Zone with your new IP.

You need the followings :

* An up-to-date ~/.aws/config file with your credentials
* Boto3 installed, ideally latest version

Then, from your terminal, just do:

```bash
  kharec@macbee ~/Desktop % path/to/updateRoute53Record.py <ZONE_ID> <RECORD.DOMAIN.FR>
```

And it's on.

Showcase:
---------
  
  Personnaly, I've got a dns that's point to my house's IP, which is dynamic. So I update my DNS "home.xxx.xxx" with that script on my Raspberry Pi, in a cron. 

**Please note that** the used service [ipinfo.io](https://ipinfo.io) supports 1000 requests a day in the free plan. So if you use this script in cron, don't plan it every minutes. There's 1440 minutes in a day. That's silly.
