#!/usr/bin/env ruby

# On stdin (or as a named file in ARGV),
# expects ascii data like motion121110_kirstiesolo.trc .
#
# On a socket, reads data like motion121110_kirstiesolo.trc .
# Format of one line:
# ["start-of-record", [-565.1, 992.3, 427.1], [-524.7, -110.1, 449.9]]

require 'rubygems'

require 'socket'

port = 4710
session = TCPSocket.new 'localhost', port
until session.closed?
  begin
    a = session.gets
    break if !a
    b = a.gsub(/[\[\],]/, '')	# strip off square brackets and commas
    c = b.split() [1..-1]	# strip "start-of-record"
    d = c.join(" ")
    File.open("consilienceIN2.dat","w") do |f|
      f.write d 
      f.write "\n"
    end
  rescue Interrupt
    fClosed=true
    puts "\nmocap client: disconnecting"
    break
  end
end
if !fClosed
  puts "mocap client: server disconnected"
  session.close
end
