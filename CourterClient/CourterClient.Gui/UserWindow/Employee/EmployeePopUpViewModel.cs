using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Security.RightsManagement;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Automation.Peers;

namespace CourterClient.Gui.Gui.UserWindow.Employee
{
    public class EmployeePopUpViewModel : ViewModelBase
    {
        private TransferGuestBooking transferGuestbooking;
        private TransferClosing transferClosing;

        private ObservableCollection<string> endsList = new ObservableCollection<string>();

        private int selectedEnd;

        public int SelectedEnd
        {
            get => selectedEnd;
            set
            {
                if (selectedEnd != value)
                {
                    selectedEnd = value;
                    RaisePropertyChanged();
                }
            }
        }

        private int CourtId { get; set; }

        private string guestname;

        public string? Guestname 
        { 
            get => guestname; 
            set
            {
                if (guestname != value)
                {
                    guestname = value;
                    RaisePropertyChanged();
                }
            }
        }

        public DateOnly Today { get; set; }
        public string CourtName { get; set; }
        public int SlotId { get; set; }

        private string endTime;
        public string EndTime
        {
            get => endTime;
            set
            {
                if (endTime != value)
                {
                    endTime = value;
                    RaisePropertyChanged();
                }
            }
        }

        private string startTime;
        public string StartTime
        {
            get => startTime;
            set
            {
                if(startTime != value)
                {
                    startTime = value;
                    RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<string> EndsList
        {
            get => endsList;
            set
            {
                if(endsList != value)
                {
                    endsList = value;
                    RaisePropertyChanged();
                }
            }
        }

        public EmployeePopUpViewModel(TransferGuestBooking guest, TransferClosing closing, DateOnly current, string courtname, int courtid, int slotId)
        {
            transferGuestbooking = guest;
            transferClosing = closing;
            Today = current;
            CourtName = courtname;
            CourtId = courtid;
            SlotId = slotId;

            GetTimeSlots();

            SetGuestbooking = new DelegateCommand((o) =>
            {
                if(Guestname != null)
                {
                    GuestBookingIn newGuestBooking = new GuestBookingIn(Today, SlotId, CourtId, Guestname);
                    transferGuestbooking.Invoke(newGuestBooking);
                }
            });

            SetClosing = new DelegateCommand(async _ =>
            {
                var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                var publicClient = root.clientManager.MakePublicClient();
                var allTimeslots = await publicClient.GetTimeslotsAsync();
                if (allTimeslots.Successful)
                {
                    var slotList = allTimeslots.Result.ToList();

                    var item = EndsList.ElementAt(SelectedEnd);

                    foreach (var slot in slotList)
                    {
                        if (slot.End.ToString() == EndsList.ElementAt(SelectedEnd))
                        {
                            ClosingIn newClosing = new ClosingIn(Today, SlotId, slot.id, CourtId);
                            transferClosing.Invoke(newClosing);
                            break;
                        }

                    }
                }

            });
        }


        private async void GetTimeSlots()
        {
            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();
            if (allTimeslots.Successful)
            {
                var slotList = allTimeslots.Result.ToList();
                int index = 0;
                foreach (var slot in slotList)
                {
                    if (slot.id == SlotId)
                    {
                        StartTime = $"{slot.Start}";
                        EndTime = $"{slot.End}";
                        for (int i = index + 1; i < slotList.Count; i++)
                        {
                            var cur = slotList[i];

                            this.EndsList.Add(cur.End.ToString());
                        }
                        break;
                    }
                    else
                    {
                        index += 1;
                    }
                }
            }
        }

        public DelegateCommand SetGuestbooking { get; set; }

        public DelegateCommand SetClosing { get; set; }
    }
}
