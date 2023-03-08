using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Media;

namespace CourterClient.Gui.Gui.UserWindow.Customer
{
    public class CustomerSlotButton : SlotButtonData
    {
        private ICustomerClient CustomerClient { get; set; }

        public CustomerSlotButton(ICustomerClient customerClient, int id, bool isBooked, bool ownBooking, string courtname, int courtid, DateOnly current)
            : base(id, isBooked, ownBooking, courtname, courtid, current)
        {
            CustomerClient = customerClient;

            BookingButtonClicked = new DelegateCommand(async _ =>
            {
                if (!IsBooked && !IsClosing && !IsPast)
                {
                    CustomerBookingIn newBooking = new CustomerBookingIn(Today, SlotId, CourtId);
                    var response = await CustomerClient.AddBookingAsync(newBooking);

                    if (response.Successful)
                    {
                        var booking = response.Result;

                        if (booking != null)
                        {
                            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                            var publicClient = root.clientManager.MakePublicClient();
                            var allTimeslots = await publicClient.GetTimeslotsAsync();
                            var allCourts = await publicClient.GetCourtsAsync();

                            if (allTimeslots.Result != null && allCourts.Result != null)
                            {
                                foreach (var time in allTimeslots.Result.ToList())
                                {
                                    if (time.id == SlotId)
                                    {
                                          MessageBox.Show($"Neue Buchung:\nDatum: {booking.Date}\nZeit: {time.Start.ToString()} - {time.End.ToString()}\nSpielfeld: {CourtName}", $"Buchung erfolgreich");
                                    }
                                }
                            }
                        }
                    }
                    IsOwnBooking = true;
                    ChangeState(true); 
                }
                else if (IsOwnBooking && IsBooked)
                {
                    var bookedSlots = await CustomerClient.GetBookingsForDateAsync(Today);

                    if (bookedSlots.Successful)
                    {
                        var result = bookedSlots.Result.ToList();

                        var todaysBookings = GetTodaysBookingOuts(result);

                        foreach (var item in todaysBookings)
                        {
                            if (item.TimeslotId == SlotId)
                            {
                                var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                                var publicClient = root.clientManager.MakePublicClient();
                                var allTimeslots = await publicClient.GetTimeslotsAsync();
                                var allCourts = await publicClient.GetCourtsAsync();

                                TimeslotOut time;
                                CourtOut court;
                                if (allTimeslots.Result != null && allCourts.Result != null)
                                {
                                    foreach (var slotItem in allTimeslots.Result.ToList())
                                    {
                                        if (slotItem.id == SlotId)
                                        {
                                            time = slotItem;
                                            foreach (var courtItem in allCourts.Result.ToList())
                                            {
                                                if (courtItem.id == CourtId)
                                                {
                                                    court = courtItem;
                                                    var deletion = await CustomerClient.DeleteBookingAsync(item.Id);
                                                    if (deletion.Successful)
                                                    {
                                                        MessageBox.Show($"Buchung gelöscht:\nDatum: {item.Date}\nZeit: {time.Start.ToString()} - {time.End.ToString()}\nSpielfeld: {court.Name}", $"Buchung storniert");
                                                        IsOwnBooking = false;
                                                        ChangeState(false);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            });
        }

        public override void SetState()
        {
            SolidColorBrush green = (SolidColorBrush)new BrushConverter().ConvertFromString("#2E8B57");
            SolidColorBrush red = (SolidColorBrush)new BrushConverter().ConvertFromString("#EE5C42");
            SolidColorBrush blue = (SolidColorBrush)new BrushConverter().ConvertFromString("#1874CD");
            SolidColorBrush past = (SolidColorBrush)new BrushConverter().ConvertFromString("Transparent");

            if (IsOwnBooking)
            {
                if (IsBooked)
                {
                    BackgroundColor = blue;
                }
                else
                {
                    BackgroundColor = green;
                }
            }
            else if (IsClosing)
            {
                BackgroundColor = red;
            }
            else if (IsPast)
            {
                BackgroundColor = past;
            }
            else
            {
                if (IsBooked)
                {
                    BackgroundColor = red;
                }
                else
                {
                    BackgroundColor = green;
                }
            }
        }
    }
}
