using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Logging;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Automation.Peers;

namespace CourterClient.Gui.Gui.UserWindow
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

        public async Task FillCourtSlots()
        {
            SlotList = new ObservableCollection<SlotButtonData>();
            var bookedSlots = await CustomerClient.GetBookingsForDateAsync(Today);

            var timeNow = DateTime.Now;

            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();

  
            if (bookedSlots.Successful)
            {
                var result = bookedSlots.Result.ToList();

                var todaysBookings = new List<BookingOut>();

                foreach(var item in result)
                {
                    if(item.Date == Today && item.CourtId == CourtId)
                    {
                        todaysBookings.Add(item);
                    }
                }

                for (int i = 0; i < Slots.Count; i++)
                {
                    TimeSlot slot = Slots[i];

                    var button = new SlotButtonData((int)slot.Id, false, false, CourtName, CourtId, CustomerClient, Today);
                    button = IsBookingPast(button, allTimeslots, timeNow);

                    foreach (var item in todaysBookings)
                    {
                        if (item.TimeslotId == slot.Id)
                        {
                            if (item.CustomerId != null)
                            {
                                button.ButtonIsBooked(true);
                                button.ButtonIsOwn(true);
                            }
                            button.ButtonIsBooked(true);
                        }

                    }
                    button.SetState();
                    SlotList.Add(button);
                }
            }
            else
            {
                MessageBox.Show($"{bookedSlots.Detail}", "Fehler");
            }
        }

        public SlotButtonData IsBookingPast(SlotButtonData button, ApiResponse<IEnumerable<TimeslotOut>> allTimeslots, DateTime timeNow)
        {
            if (allTimeslots.Result != null)
            {
                TimeslotOut time;
                foreach (var item in allTimeslots.Result.ToList())
                {
                    if (Today == DateOnly.FromDateTime(timeNow) && TimeOnly.FromDateTime(timeNow) > item.Start)
                    {
                        if (item.id == button.Id)
                        {
                            button.IsButtonEnabled(false);
                        }
                    }
                    else if(Today < DateOnly.FromDateTime(timeNow))
                    {
                        if (item.id == button.Id)
                        {
                            button.IsButtonEnabled(false);
                        }
                    }
                }
            }
            return button;
        }
    }
}
