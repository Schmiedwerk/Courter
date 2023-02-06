using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui
{
    public class TimeSlot
    {
        public string Start { get; set; }
        public string End { get; set; }
        public string Hyphen { get; set; }

        public TimeSlot(string start, string end)
        {
            Start = start;
            End = end;
            if(start == "" || end == "")
            {
                Hyphen = "";
            }
            else
            {
                Hyphen = "-";
            }
        }
    }
}
