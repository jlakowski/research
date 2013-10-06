#!/usr/bin/env ruby

# repeatedly read a file consilienceOUT.dat,
# a sequence of whitespace-delimited floats ending with a newline.
# Continuously broadcast THAT.

require 'rubygems'

puts "mocap server: ready for clients"

require 'socket'
port = 4710
server = TCPServer.new 'localhost', port
loop do
  begin
    Thread.start(server.accept) do |session|
      puts "mocap server: new client connected"
      fClosed = false
      until session.closed?
	begin
          $d = (fd = File.open("consilienceOUT.dat", "r")).map &:chomp
	  fd.close
	  session.print "#{$d.inspect}\n"
	rescue
	  fClosed=true
	  puts "mocap server: client disconnected"
	  break
	end
	sleep 0.05    # 20 Hz while we're writing this code
      end
      if !fClosed
	puts "mocap server: disconnecting"
	session.close
      end
    end
  rescue Interrupt
    puts "\nmocap server: terminating"
    exit
  end
end
