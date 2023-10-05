# GW Astrology

## Statement of Purpose
**Disclaimer: We are physicists NOT astrologers, you should not plan your life on our horoscopes**

This is pop cultural scientific activity. The purpose is to alert people of gravitational waves in a fun way, by using astrology.
Subscribers will receive alerts of gravitational waves including a fact sheet of basic event info, a "GW birth chart" and horoscope.

## Design

### GW Birth Chart

* Sun sign: map RA/Dec to constellation and assign sun sign
* Rising: map time of coalescence to rising sign
* Moon: map time and highest SNR detector location to moon sign

### Astrological Weather Report

Given GW event time, calculate the sun and moon's current sky position, maybe other things.
Generate a horoscope from this information.

- start with an adlib horoscope template
- an array of fill-in words
- map sun, moon, etc. current sky position to index 
   - aquarius = index + 0 
   - pisces = index + 1
   - etc.
- use those words to fill in the horoscope

## Instructions

1. Set up SCiMMA credentials by following instructions here: https://computing.docs.ligo.org/igwn-alert/client/guide.html#managing-credentials-and-topics
2. In your run dir do `make env` then `source env.sh`
3. After you have been added to the `lvk-users` group and created a credential, download the csv file and in your run dir do: `hop auth add <csv file>`
4. Run the listener: `python3 igwn-alert-listener`
