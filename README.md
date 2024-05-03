# easy-loxone-influx


## What is it good for?

This tutorial shows you how to easily send Loxone statistics to InfluxDB 1.8 timescale database through UDP messages. Once you have your data stored InfluxDB, you can visualize them with Grafana.

<img src="./pics/00.png" alt="00" style="zoom:100%;" />

## How to connect Loxone to InfluxDB?

In contrast to most other solutions and tutorials, this one does not use websockets for sending statistics from Loxone, but simple UDP (or HTTP) messages. It is very easy to setup and use. The configuration of individual measurements and statistics is done through Loxone Config. 

There are essentially two solutions. Both of them allow you to set measurement names and tags for your statistics within Loxone Config. Choose for yourself and go to more detailed tutorial below:

### 1. UDP logger

**Pros:**

* Easily attach UDP Logger to most objects in Loxone Config (no need to draw program in Loxone Config). 

**Cons:**

* Needs external Python script.
* Messages sent by Loxone utilize custom syntax.
* Loxone logger can only send statistics via UDP, not HTTP(S).

Here is a quick look at how it works:

<img src="./pics/02.png" alt="02" style="zoom:100%;" />

For detailed instructions, go to a [UDP LOGGER -> INFLUXDB TUTORIAL](https://github.com/budulinek/easy-loxone-influx/blob/master/1.UDP%20logger.md) .

### 2. Virtual output

**Pros:**

* Direct connection between Loxone and InfluxDB (no external script or third-party software).
* Messages sent by Loxone comply to [InfluxDB line protocol](https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/).
* Virtual output can send statistics either via UDP or HTTP(S) messages.

**Cons:**

* Requires you to draw a program in Loxone Config.

Here is a quick look at how it works:

<img src="./pics/10.png" alt="10" style="zoom:100%;" />

For detailed instructions, go to a [VIRTUAL OPUTPUT -> INFLUXDB TUTORIAL](https://github.com/budulinek/easy-loxone-influx/blob/master/2.Virtual%20output.md) .
