NAME

::

    ZELF - the self


DESCRIPTION


::

    ZELF is a python3 IRC bot is intended to be programmable in a
    static, only code, no popen, no user imports and no reading
    modules from a directory, way. 

    ZELF provides some functionality, it can connect to IRC, fetch
    and display RSS feeds, take todo notes, keep a shopping list and
    log text.


SYNOPSIS


::

    zelf <cmd> [key=val] 
    zelf <cmd> [key==val]
    zelf [-c] [-d] [-v]


INSTALL


::

    $ pipx install zelf

USAGE


::

    for ease of use, use an alias

    $ alias zelf="python3 -m zelf"

    list of commands

    $ zelf cmd
    cmd,err,flt,sts,thr,upt

    start a console

    $ zelf -c
    >

    start additional modules

    $ zelf mod=<mod1,mod2> -c
    >

    list of modules

    $ zelf mod
    bsc,err,flt,irc,log,mod,rss,shp,
    sts,tdo,thr,udp

    to start irc, add mod=irc when
    starting

    $ zelf -c mod=irc

    to start rss, also add mod=rss
    when starting

    $ zelf -c mod=irc,rs

    start as daemon

    $ zelf -d mod=irc,rss
    $ 


CONFIGURATION


::

    irc

    $ zelf cfg server=<server>
    $ zelf cfg channel=<channel>
    $ zelf cfg nick=<nick>

    sasl

    $ zelf pwd <nsvnick> <nspass>
    $ zelf cfg password=<frompwd>

    rss

    $ zelf rss <url>
    $ zelf dpl <url> <item1,item2>
    $ zelf rem <url>
    $ zelf nme <url< <name>


COMMANDS


::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    flt - instances registered
    log - log some text
    met - add user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    thr - show the running threads


SYSTEMD

::

    [Unit]
    Description=ZELF - the self
    Requires=network.target
    After=network.target

    [Service]
    DynamicUser=True
    Type=forking
    User=bart
    Group=bart
    PIDFile=/home/bart/.zelf/zelf.pid
    WorkingDirectory=/home/bart/.zelf
    ExecStart=/home/bart/.local/pipx/venvs/zelf/bin/zelf -d mod=irc,rss
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


FILES

::

    ~/.local/bin/zelf
    ~/.local/pipx/venvs/zelf/


AUTHOR

::

    Zelf <tehzelf@gmail.com>


COPYRIGHT

::

    ZELF is placed in the Public Domain.
