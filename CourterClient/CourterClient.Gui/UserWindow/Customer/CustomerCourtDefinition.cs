using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;

namespace CourterClient.Gui.Gui.UserWindow.Customer
{
    public class CustomerCourtDefinition : CourtDefinition
    {
        ICustomerClient CustomerClient { get; set; }
        public CustomerCourtDefinition(ICustomerClient customerClient, string courtName, int id, List<TimeSlot> slots, DateOnly current)
            : base(courtName, id, slots, current)
        {
            CustomerClient = customerClient;

            FillCourtSlots();
        }

        public override async Task FillCourtSlots()
        {
            SlotList = new ObservableCollection<SlotButtonData>();
            var bookedSlots = await CustomerClient.GetBookingsForDateAsync(Today);
            var timeNow = DateTime.Now;
            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();
            var bookedClosings = await publicClient.GetClosingsForDateAsync(Today);


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
                    var button = new CustomerSlotButton(CustomerClient, (int)slot.Id, false, false, CourtName, CourtId, Today);
                    button.IsBookingPast(timeslotList, timeNow);
                    button.CheckBooking(todaysBookings, slot);
                    button.CheckClosings(todaysClosings, slot);
                    button.SetState();
                    SlotList.Add(button);
                }
            }
            else
            {
                MessageBox.Show($"{bookedSlots.Detail}", "Fehler");
            }
        }
    }
}
