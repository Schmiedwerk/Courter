using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Reflection.Metadata.BlobBuilder;

namespace CourterClient.Gui.Gui.UserWindow
{
    class UserViewModel : ViewModelBase
    {
        private ObservableCollection<TimeSlot> timeSlots = new ObservableCollection<TimeSlot>();
        private ObservableCollection<CourtDefinition> courts = new ObservableCollection<CourtDefinition>();
        public List<CourtDefinition> courtList = new List<CourtDefinition>();
        private int Slots = 0;

        public ObservableCollection<TimeSlot> TimeSlots
        {
            get => timeSlots;
            set
            {
                if(timeSlots!= value)
                {
                    timeSlots = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<CourtDefinition> Courts
        {
            get => courts;
            set
            {
                if(courts!= value)
                {
                    courts = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public UserViewModel()
        {
            CreateTimeTable(10, 22);
            AddCourt("Wimbledon", Slots);
            AddCourt("New York", Slots);
            AddCourt("Melbourne", Slots);
            AddCourt("Paris", Slots);

            CreateCourtTable();
        }


        public void CreateTimeTable(int startVal, int endVal)
        {
            this.TimeSlots = new ObservableCollection<TimeSlot>();
            {
                this.TimeSlots.Add(new TimeSlot("", ""));
                for (int i = startVal; i <= endVal - 1; i++)
                {
                    string start = $"{i}:00";
                    string end = $"{i + 1}:00";
                    var item = new TimeSlot(start, end);
                    this.TimeSlots.Add(item);
                    this.Slots++;
                }
            }
        }

        public void AddCourt(string courtName, int slots)
        {
            CourtDefinition newCourt = new CourtDefinition(courtName, slots);
            this.courtList.Add(newCourt);
        }

        public void CreateCourtTable()
        {
            this.Courts= new ObservableCollection<CourtDefinition>();
            {
                foreach (var item in this.courtList)
                {
                    this.Courts.Add(item);
                }
            }
        }
    }
}
