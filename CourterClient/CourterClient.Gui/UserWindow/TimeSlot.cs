using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    public class TimeSlot
    {
        public int? Id {  get; set; }
        public string Start { get; set; }
        public string End { get; set; }
        public string Hyphen { get; set; }

        public TimeSlot(string start, string end, int id)
        {
            Id = id;
            Start = start;
            End = end;
            Hyphen = "-";
        }

        public TimeSlot()
        {
            Id = null;
            Start = "";
            End = "";
            Hyphen = "";
        }
    }
}
