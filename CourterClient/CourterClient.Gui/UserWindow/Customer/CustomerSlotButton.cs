using CourterClient.ApiClient;
using CourterClient.Gui.Gui.PopUpWindows;
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
                                        List<string> info = new List<string>();
                                        info.Add("Neue Buchung:");
                                        info.Add(booking.Date.ToString());
                                        info.Add(CourtName);
                                        info.Add(time.Start.ToString());
                                        info.Add(time.End.ToString());
                                        var InfoView = new InfoView(info);
                                        InfoView.ShowDialog();
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
                                                    List<string> info = new List<string>();
                                                    info.Add("Buchung stornieren?");
                                                    info.Add(item.Date.ToString());
                                                    info.Add(CourtName);
                                                    info.Add(time.Start.ToString());
                                                    info.Add(time.End.ToString());

                                                    var question = new DeleteView(info, transferResponse);
                                                    question.ShowDialog();
                                                    if(Response)
                                                    {
                                                        court = courtItem;
                                                        var deletion = await CustomerClient.DeleteBookingAsync(item.Id);
                                                        if (deletion.Successful)
                                                        {
                                                            info = new List<string>();
                                                            info.Add("Buchung gelöscht:");
                                                            info.Add(item.Date.ToString());
                                                            info.Add(court.Name);
                                                            info.Add(time.Start.ToString());
                                                            info.Add(time.End.ToString());
                                                            var InfoView = new InfoView(info);
                                                            InfoView.ShowDialog();
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
