using CourterClient.ApiClient;
using CourterClient.Gui.CalendarWindow;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    class UserViewModel : ViewModelBase
    {
        public TransferDate delegateTransfer;
        private ClientManager ClientManager { get; set; }
        private IPublicClient publicClient { get; set; }
        private ObservableCollection<TimeSlot> timeSlots = new ObservableCollection<TimeSlot>();
        private ObservableCollection<CourtDefinition> courts = new ObservableCollection<CourtDefinition>();
        private int Slots = 0;

        public DateManager DateManager { get; set; }    

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

        public UserViewModel(ClientManager rootClient)
        {
            ClientManager = rootClient;
            publicClient = ClientManager.clientManager.MakePublicClient();

            DateManager = new DateManager();
            delegateTransfer += new TransferDate(SetCurrentDate);

            SetNextDay = new DelegateCommand((o) =>
            {
                DateManager.SetDate(DateManager.Next);
            });

            SetPreviousDay = new DelegateCommand((o) =>
            {
                DateManager.SetDate(DateManager.Previous);
            });

            OpenCalendar = new DelegateCommand((o) =>
            {
                var cal = new CalendarView(delegateTransfer);
                cal.ShowDialog();
            });
        }

        public async Task CreateTimeTable()
        {
            var remoteTimeslots = await publicClient.GetTimeslotsAsync();

            if(remoteTimeslots.Successful)
            {
                List<TimeslotOut> remoteTimeslotList = remoteTimeslots.Result.ToList();
                this.TimeSlots = new ObservableCollection<TimeSlot>();
                {
                    this.TimeSlots.Add(new TimeSlot("", ""));
                    foreach (var time in remoteTimeslotList)
                    {
                        string start = $"{Convert.ToString(time.Start)}";
                        string end = $"{Convert.ToString(time.End)}";
                        var item = new TimeSlot(start, end);
                        this.TimeSlots.Add(item);
                        this.Slots++;
                    }
                }
            }
        }

        public async Task CreateCourtTable()
        {
            var remoteCourts = await publicClient.GetCourtsAsync();
            if(remoteCourts.Successful)
            {
                List<CourtOut> remoteCourtList = remoteCourts.Result.ToList();
                this.Courts = new ObservableCollection<CourtDefinition>();
                {
                    foreach (var court in remoteCourtList)
                    {
                        var item = new CourtDefinition(court.Name, Slots);
                        this.Courts.Add(item);
                    }
                }
            }
        }

        public void SetCurrentDate(DateOnly date)
        {
            this.DateManager.SetDate(date);
        }

        public DelegateCommand SetNextDay { get; set; }

        public DelegateCommand SetPreviousDay { get; set; }

        public DelegateCommand OpenCalendar { get; set; }
    }
}
