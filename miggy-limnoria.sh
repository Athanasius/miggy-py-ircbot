#!/bin/sh

exec supybot \
	--nick=Cmdr \
	--user="Cmdr Jameson - the original cmdr edbot@miggy.org" \
	--ident="cmdr" \
	--debug \
	$@

