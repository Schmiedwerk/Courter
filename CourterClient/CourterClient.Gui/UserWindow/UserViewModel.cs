using CourterClient.ApiClient;
using CourterClient.Gui.CalendarWindow;
using CourterClient.Gui.Gui.UserWindow.Customer;
using CourterClient.Gui.Gui.UserWindow.Employee;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    public class UserViewModel : ViewModelBase
    {
        public TransferDate delegateTransfer;
        public IPublicClient PublicClient { get; set; }
        public IEmployeeClient? EmployeeClient { get; set; }
        public ICustomerClient? CustomerClient { get; set; }

        private ObservableCollection<TimeSlot> timeSlots = new ObservableCollection<TimeSlot>();
        private ObservableCollection<CourtDefinition> courts = new ObservableCollection<CourtDefinition>();
        public List<TimeSlot> Slots;

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

        public UserViewModel(IPublicClient publicClient, IEmployeeClient employeeClient)
        {
            PublicClient = publicClient;
            EmployeeClient = employeeClient;

            DateManager = new DateManager();
            delegateTransfer += new TransferDate(SetCurrentDate);

            SetNextDay = new DelegateCommand(async (o) =>
            {
                DateManager.SetDate(DateManager.Next);
                await CreateCourtTable();
            });

            SetPreviousDay = new DelegateCommand(async (o) =>
            {
                DateManager.SetDate(DateManager.Previous);
                await CreateCourtTable();
            });

            OpenCalendar = new DelegateCommand((o) =>
            {
                var cal = new CalendarView(delegateTransfer);
                cal.ShowDialog();
            });
        }

        public UserViewModel(IPublicClient publicClient, ICustomerClient customerClient)
        {
            PublicClient = publicClient;
            CustomerClient = customerClient;

            DateManager = new DateManager();
            delegateTransfer += new TransferDate(SetCurrentDate);

            SetNextDay = new DelegateCommand(async (o) =>
            {
                DateManager.SetDate(DateManager.Next);
                await CreateCourtTable();
            });

            SetPreviousDay = new DelegateCommand(async (o) =>
            {
                DateManager.SetDate(DateManager.Previous);
                await CreateCourtTable();
            });

            OpenCalendar = new DelegateCommand((o) =>
            {
                var cal = new CalendarView(delegateTransfer);
                cal.ShowDialog();
            });
        }

        public async Task CreateTimeTable()
        {
            var remoteTimeslots = await PublicClient.GetTimeslotsAsync();

            if(remoteTimeslots.Successful)
            {
                List<TimeslotOut> remoteTimeslotList = remoteTimeslots.Result.ToList();
                Slots = new List<TimeSlot>();
                this.TimeSlots = new ObservableCollection<TimeSlot>();
                {
                    this.TimeSlots.Add(new TimeSlot());
                    foreach (var time in remoteTimeslotList)
                    {
                        string start = $"{Convert.ToString(time.Start)}";
                        string end = $"{Convert.ToString(time.End)}";
                        var item = new TimeSlot(start, end, time.id);
                        this.Slots.Add(item);
                        this.TimeSlots.Add(item);
                    }
                }
            }
        }

        public async Task CreateCourtTable()
        {
            var remoteCourts = await PublicClient.GetCourtsAsync();

            if (remoteCourts.Successful)
            {
                List<CourtOut> remoteCourtList = remoteCourts.Result.ToList();

                this.Courts = new ObservableCollection<CourtDefinition>();
                {
                    foreach (var court in remoteCourtList)
                    {
                        if(EmployeeClient != null)
                        {
                            var item = new EmployeeCourtDefinition(EmployeeClient, court.Name, court.id, Slots, DateManager.Current);
                            this.Courts.Add(item);
                        }
                        else if(CustomerClient != null)
                        {
                            var item = new CustomerCourtDefinition(CustomerClient, court.Name, court.id, Slots, DateManager.Current);
                            this.Courts.Add(item);
                        }
                    }
                }
            }
        }

        public async void SetCurrentDate(DateOnly date)
        {
            this.DateManager.SetDate(date);
            await CreateCourtTable();
        }

        public DelegateCommand SetNextDay { get; set; }

        public DelegateCommand SetPreviousDay { get; set; }

        public DelegateCommand OpenCalendar { get; set; }
    }
}
