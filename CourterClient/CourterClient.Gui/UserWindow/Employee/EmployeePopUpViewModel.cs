using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows.Documents;

namespace CourterClient.Gui.Gui.UserWindow.Employee
{
    public class EmployeePopUpViewModel : ViewModelBase
    {
        private IEmployeeClient EmployeeClient { get; set; }
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

        public EmployeePopUpViewModel(IEmployeeClient employeeClient ,TransferGuestBooking guest, TransferClosing closing, DateOnly current, string courtname, int courtid, int slotId)
        {
            EmployeeClient = employeeClient;
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
            var bookingsToday = await EmployeeClient.GetBookingsForDateAsync(Today);

            if (allTimeslots.Successful && bookingsToday.Successful)
            {
                var slotList = allTimeslots.Result.ToList();

                foreach (var slot in slotList)
                {
                    if (slot.id == SlotId)
                    {
                        StartTime = $"{slot.Start}";
                        EndTime = $"{slot.End}";

                        BookingOut nextBooking = null;

                        foreach (var booking in bookingsToday.Result.ToList()) 
                        {
                            if(booking.Date == Today && booking.CourtId == CourtId)
                            {
                                if (booking.TimeslotId >= SlotId)
                                {
                                    nextBooking = booking;
                                }
                            }
                        }
                        for (int i = 0; i < slotList.Count; i++)
                        {
                            if (nextBooking != null)
                            {
                                if (slotList[i].id >= slot.id && slotList[i].id < nextBooking.TimeslotId)
                                {
                                    this.EndsList.Add(slotList[i].End.ToString());
                                }
                            }
                            else
                            {
                                if (slotList[i].id >= slot.id)
                                {
                                    this.EndsList.Add(slotList[i].End.ToString());
                                }
                            }
                        }
                    }
                }
            }
        }

        public DelegateCommand SetGuestbooking { get; set; }

        public DelegateCommand SetClosing { get; set; }
    }
}
