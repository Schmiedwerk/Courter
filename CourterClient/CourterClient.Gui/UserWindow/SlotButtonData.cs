using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Automation.Peers;
using System.Windows.Media;

namespace CourterClient.Gui.Gui.UserWindow
{
    public class SlotButtonData : ViewModelBase
    {
        private string CourtName { get; set; }
        private int CourtId { get; set; }
        public int Id { get; set; }
        private bool IsBooked { get; set; }


        private ICustomerClient CustomerClient { get; set; }

        private DateOnly Today { get; set; }

        private bool IsOwnBooking { get; set; }

        private bool enableButton;
        public bool EnableButton
        {
            get => enableButton;
            set
            {
                if(enableButton != value)
                {
                    enableButton = value;
                    RaisePropertyChanged();
                }
            }
        }

        private SolidColorBrush backgroundColor;
        
        public SolidColorBrush BackgroundColor
        {
            get=> backgroundColor;
            set
            {
                if(backgroundColor != value)
                {
                    backgroundColor = value;
                    RaisePropertyChanged();
                }
            }
        }

        public SlotButtonData(int id, bool isBooked, bool ownBooking, string courtname, int courtid, ICustomerClient customerClient, DateOnly current)
        {
            EnableButton = true;
            CourtName = courtname;
            CourtId = courtid;
            Id = id;
            IsBooked = isBooked;
            IsOwnBooking = ownBooking;
            CustomerClient = customerClient;
            Today = current;

            BookingButtonClicked = new DelegateCommand( async _ =>
            {
                if (!IsBooked)
                {
                    CustomerBookingIn newBooking = new CustomerBookingIn(Today, Id, CourtId);
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
                                TimeslotOut time;
                                CourtOut court;

                                foreach(var item in allTimeslots.Result.ToList())
                                {
                                    if(item.id == Id)
                                    {
                                        time = item;
                                        foreach (var item2 in allCourts.Result.ToList())
                                        {
                                            if (item2.id == CourtId)
                                            {
                                                court = item2;
                                                MessageBox.Show($"Neue Buchung:\nDatum: {booking.Date}\nZeit: {time.Start.ToString()} - {time.End.ToString()}\nSpielfeld: {court.Name}", $"Buchung Erfolgreich");
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    IsOwnBooking = true;
                    ChangeState(true);
                }
                //else
                //{
                //    ChangeState(false);
                //}

            });
        }

        public void SetState()
        {
            SolidColorBrush green = (SolidColorBrush)new BrushConverter().ConvertFromString("#6f916f");
            SolidColorBrush red = (SolidColorBrush)new BrushConverter().ConvertFromString("#EE5C42");
            SolidColorBrush blue = (SolidColorBrush)new BrushConverter().ConvertFromString("#5F9EA0");
            //Set state needs to disable buttons which timeslots are in the past.

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

        public void ChangeState(bool booking)
        {
            IsBooked = booking;

            SetState();
        }

        public void IsButtonEnabled(bool enabled)
        {
            this.EnableButton = enabled;

        }

        public void ButtonIsBooked(bool isBooked)
        {
            this.IsBooked = isBooked;
        }

        public void ButtonIsOwn(bool isOwnBooking)
        {
            this.IsOwnBooking = isOwnBooking;
        }

        public DelegateCommand BookingButtonClicked { get; set; }

    }
}
