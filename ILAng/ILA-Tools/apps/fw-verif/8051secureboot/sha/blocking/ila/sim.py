# A simple simulator for SHA+XRAM

from mmio import mmiodev, NOP, RD, WR
import sha as SHAFunc

def as_chars (s, n):
    b = []
    for i in xrange (n):
        byte = s & 0xff
        s >>= 8
        b.append (byte)
    return [chr (i) for i in b]

def to_num (s, n):
    num = 0
    for i in xrange (n):
        num |= (ord (s[i]) << (i * 8))
    return num

class SHA (mmiodev):
    SHA_IDLE = 0
    SHA_RD   = 1
    SHA_OP1  = 2
    SHA_OP2  = 3
    SHA_WR   = 4

    CMD_RD   = 1
    CMD_WR   = 2

    def __init__ (self):
        mmiodev.__init__ (self)
        self.addReg ('sha_start', 0xfe00, 1, readonly = True)
        self.addReg ('sha_state', 0xfe01, 1, readonly = True)
        self.addReg ('sha_rdaddr', 0xfe04, 2)
        self.addReg ('sha_wraddr', 0xfe08, 2)
        self.addReg ('sha_len', 0xfe0c, 2)

        self.rd_data = [0] * 64
        self.hs_data = [0] * 20

        self.sha = SHAFunc.new()

    # Create easy access properties.
    sha_state  = property (lambda s: s.getRegI ('sha_state'), lambda s, v: s.setRegI ('sha_state', v))
    sha_rdaddr = property (lambda s: s.getRegI ('sha_rdaddr'), lambda s, v: s.setRegI ('sha_rdaddr', v))
    sha_wraddr = property (lambda s: s.getRegI ('sha_wraddr'), lambda s, v: s.setRegI ('sha_wraddr', v))
    sha_len    = property (lambda s: s.getRegI ('sha_len'), lambda s, v: s.setRegI ('sha_len', v))

    def simulate (self, s_in):
        cmd     = s_in['cmd']
        cmdaddr = s_in['cmdaddr']
        cmddata = s_in['cmddata']

        self.sha_state  = s_in['sha_state']
        self.sha_rdaddr = s_in['sha_rdaddr']
        self.sha_wraddr = s_in['sha_wraddr']
        self.sha_len    = s_in['sha_len']
        self.rd_data    = s_in['sha_rd_data']
        self.hs_data    = s_in['sha_hs_data']
        self.xram       = s_in['XRAM']
        self.bytes_read = s_in['sha_bytes_read']

        # execute command.
        state_nxt = self.sha_state
        if self.sha_state == self.SHA_IDLE:
            if cmd == WR:
                if cmdaddr == 0xfe00:
                    if cmddata == 1:
                        state_nxt = self.SHA_RD
                        self.bytes_read = 0
                else:
                    self.write (cmdaddr, cmddata)
        elif self.sha_state == self.SHA_RD:
            state_nxt = self.SHA_OP1
            self.bytes_read = self.bytes_read + 64
            # FIXME 
            # self.rd_data = 
        elif self.sha_state == self.SHA_OP1:
            state_nxt = self.SHA_OP2
        elif self.sha_state == self.SHA_OP2:
            if self.bytes_read < self.sha_len:
                state_nxt = self.SHA_RD
                # FIXME
                # self.hs_data = 
            else:
                state_nxt = self.SHA_WR
        elif self.sha_state == self.SHA_WR:
            for i in xrange (20):
                addr = (self.sha_wraddr + 19 - i) & 0xffff
                byte = self.hs_data >> (i*8) & 0xff
                self.xram[addr] = byte
            state_nxt = self.SHA_IDLE

        self.sha_state = state_nxt

        s_out = self.s_dict()
        return s_out

    def s_dict (self):
        return {
            'sha_state'     : self.sha_state,
            'sha_rdaddr'    : self.sha_rdaddr,
            'sha_wraddr'    : self.sha_wraddr,
            'sha_len'       : self.sha_len,
            'sha_rd_data'   : self.rd_data,
            'sha_hs_data'   : self.hs_data,
            'XRAM'          : self.xram,
            'sha_bytes_read': self.bytes_read
        }
