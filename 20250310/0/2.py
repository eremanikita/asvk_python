import calendar
import readline
import cmd


class show_calend(cmd.Cmd):
    prompt = "cmd>> "
    cal = calendar.TextCalendar()
    month = {m.name: m.value for m in calendar.Month}

    def do_prmonth(self, arg):
        """Print a month’s calendar as returned by formatmonth()."""
        year, month = arg.split()
        self.cal.prmonth(int(year), self.month[month])

    def do_pryear(self, arg):
        """Print the calendar for an entire year as returned by formatyear()."""
        self.cal.pryear(*map(int, arg.split()))

    def complete_prmonth(self, text, line, begidx, endidx):
        return [c for c in self.month if c.startswith(text)]


if __name__ == '__main__':
    readline.parse_and_bind("bind ^I rl_complete")
    show_calend().cmdloop()
