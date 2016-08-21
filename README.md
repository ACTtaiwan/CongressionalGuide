# ACT U.S. Congressional Guide
Provides code to allow users to look up members and candidates for the U.S. Congress to see if they support certain legislation or issues.

The ACT U.S. Congressional Guide is an open-source project to provide organizations with a guide for users to look up candidates during an election, and members of Congress the rest of the time on specific issues and bills.
* A voter guide during election periods.
* Method for users to use social media or email to ask for a questionnaire to be answered.
* During non-election periods, a guide showing current members of Congress support for certain legislation and issues.
* Rather than a separate site, this is designed to be integrated with an existing website.

To find out more, please check out the [Congressional Guide wiki](https://github.com/ACTtaiwan/CongressionalGuide/wiki/About-the-ACT-U.S.-Congressional-Guide).

## Architecture Design
* The [Express](http://expressjs.com) framework for [Node.js](https://nodejs.org/en/) is used for a foundation.
* Storage: [SQLite](http://sqlite.org) - see [here](http://expressjs.com/en/guide/database-integration.html#sqlite) for SQLite Express DB intagration.
* For [npm](https://www.npmjs.com) packages used, see the `app/package.json` file.

## Getting Started
To get a local environment up and running, start with the `app/README.md`

# Throughput Graph
[![Throughput Graph](https://graphs.waffle.io/ACTtaiwan/CongressionalGuide/throughput.svg)](https://waffle.io/ACTtaiwan/CongressionalGuide/metrics/throughput)
