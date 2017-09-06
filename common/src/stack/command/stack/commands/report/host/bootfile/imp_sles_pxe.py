# @SI_Copyright@
# @SI_Copyright@

import stack.commands
from stack.exception import *

class Implementation(stack.commands.Implementation):
	def run(self, h):

		host	 = h['host']
		ip	 = h['ip']
		mask	 = h['mask']
		gateway	 = h['gateway']
		kernel	 = h['kernel']
		ramdisk	 = h['ramdisk']
		args	 = h['args']
		filename = h['filename']
		attrs	 = h['attrs']
		action	 = h['action']
		boottype = h['type']

		self.owner.addOutput(host,'default stack')
		self.owner.addOutput(host,'prompt 0')
		self.owner.addOutput(host,'label stack')

		if kernel:
			if kernel[0:7] == 'vmlinuz':
				self.owner.addOutput(host,'\tkernel %s' % (kernel))
			else:
				self.owner.addOutput(host,'\t%s' % (kernel))
		if ramdisk and len(ramdisk) > 0:
			if len(args) > 0:
				args += ' initrd=%s' % ramdisk
			else:
				args = 'initrd=%s' % ramdisk

		if args and len(args) > 0:
			self.owner.addOutput(host,'\tappend %s' % args)
		if boottype == "install":
			self.owner.addOutput(host,'\tipappend 2')