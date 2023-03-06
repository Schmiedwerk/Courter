using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Automation.Peers;

namespace CourterClient.Gui.Gui.UserWindow.Employee
{
    public class EmployeeCourtDefinition : CourtDefinition
    {
        IEmployeeClient EmployeeClient { get; set; }
        public TransferCourtDefinitionTrigger TransferCourtDefinitionTrigger;

        public EmployeeCourtDefinition(IEmployeeClient employeeClient, string courtName, int id, List<TimeSlot> slots, DateOnly current)
            : base(courtName, id, slots, current)
        {
            EmployeeClient = employeeClient;
            TransferCourtDefinitionTrigger += new TransferCourtDefinitionTrigger(FillCourtSlots);

            FillCourtSlots();
        }

        public override async Task FillCourtSlots()
        {
            SlotList = new ObservableCollection<SlotButtonData>();
            var bookedSlots = await EmployeeClient.GetBookingsForDateAsync(Today);
            var bookedClosings = await EmployeeClient.GetClosingsForDateAsync(Today);

            var timeNow = DateTime.Now;

            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();

            if (bookedSlots.Successful && bookedClosings.Successful)
            {
                var bookingResults = bookedSlots.Result.ToList();
                var closingResults = bookedClosings.Result.ToList();

                var todaysBookings = new List<BookingOut>();

                var todaysClosings = new List<ClosingOut>();

                foreach (var item in bookingResults)
                {
                    if (item.Date == Today && item.CourtId == CourtId)
                    {
                        todaysBookings.Add(item);
                    }
                }

                foreach (var close in  closingResults)
                {
                    if(close.Date == Today && close.CourtId == CourtId)
                    {
                        todaysClosings.Add(close);
                    }
                }

                for (int i = 0; i < Slots.Count; i++)
                {
                    TimeSlot slot = Slots[i];

                    var button = new EmployeeSlotButton(EmployeeClient, TransferCourtDefinitionTrigger, (int)slot.Id, false, false, CourtName, CourtId, Today);
                    button = (EmployeeSlotButton)IsBookingPast(button, allTimeslots, timeNow);

                    foreach (var item in todaysBookings)
                    {
                        if (item.TimeslotId == slot.Id)
                        {
                            if (item.GuestName != null)
                            {
                                button.GuestName = item.GuestName;
                            }
                            button.IsBooked = true;
                        }
                    }

                    foreach (var item in todaysClosings)
                    {
                        if(item.StartTimeslotId <=  slot.Id && item.EndTimeslotId >= slot.Id)
                        {
                            button.IsClosing = true;
                        }
                    }

                    button.SetState();
                    SlotList.Add(button);
                }
            }
        }
    }
}
