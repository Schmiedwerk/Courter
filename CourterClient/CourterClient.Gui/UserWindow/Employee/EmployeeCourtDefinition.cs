using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;

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
            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();
            var bookedClosings = await publicClient.GetClosingsForDateAsync(Today);

            var timeNow = DateTime.Now;


            if (bookedSlots.Successful && bookedClosings.Successful)
            {
                var bookingResults = bookedSlots.Result.ToList();
                var closingResults = bookedClosings.Result.ToList();

                var todaysBookings = GetTodaysBookingOuts(bookingResults);
                var todaysClosings = GetTodaysClosingOuts(closingResults);

                var timeslotList = allTimeslots.Result.ToList();

                for (int i = 0; i < Slots.Count; i++)
                {
                    TimeSlot slot = Slots[i];

                    var button = new EmployeeSlotButton(EmployeeClient, TransferCourtDefinitionTrigger, (int)slot.Id, false, false, CourtName, CourtId, Today);
                    button.IsBookingPast(timeslotList, timeNow);
                    button.CheckGuestname(todaysBookings, slot);
                    button.CheckClosings(todaysClosings, slot);

                    button.SetState();
                    SlotList.Add(button);
                }
            }
        }
    }
}
