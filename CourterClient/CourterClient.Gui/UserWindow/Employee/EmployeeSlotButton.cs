using CourterClient.ApiClient;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;

namespace CourterClient.Gui.Gui.UserWindow.Employee
{
    public class EmployeeSlotButton : SlotButtonData
    {
        public TransferGuestBooking? newGuestBooking;
        public TransferClosing? newClosing;

        private TransferCourtDefinitionTrigger? newCourtDefinitionTrigger;

        private IEmployeeClient EmployeeClient { get; set; }

        private EmployeePopUpView empWindow;

        public bool IsClosing { get; set; }

        private string? guestName;
        public string? GuestName
        {
            get => guestName;
            set
            {
                if (guestName != value)
                {
                    guestName = value;
                    RaisePropertyChanged();
                }
            }
        }

        public EmployeeSlotButton(IEmployeeClient employeeClient, TransferCourtDefinitionTrigger newCourt, int id, bool isBooked, bool ownBooking, string courtname, int courtid, DateOnly current)
            : base(id, isBooked, ownBooking, courtname, courtid, current)
        {
            EmployeeClient = employeeClient;
            newCourtDefinitionTrigger = newCourt;

            newGuestBooking += new TransferGuestBooking(AddGuestbooking);

            newClosing += new TransferClosing(AddClosing);

            BookingButtonClicked = new DelegateCommand(async _ =>
            {
                if (!IsBooked && !IsClosing)
                {
                    var empWinVM = new EmployeePopUpViewModel(newGuestBooking, newClosing, Today, CourtName, CourtId, SlotId);
                    empWindow = new EmployeePopUpView();
                    empWindow.DataContext = empWinVM;
                    empWindow.ShowDialog();
                }
                else if(IsBooked && GuestName != null)
                {
                    var bookedSlots = await EmployeeClient.GetBookingsForDateAsync(Today);

                    if (bookedSlots.Successful)
                    {
                        var result = bookedSlots.Result.ToList();

                        var todaysBookings = new List<BookingOut>();

                        foreach (var item in result)
                        {
                            if (item.Date == Today && item.CourtId == CourtId)
                            {
                                todaysBookings.Add(item);
                            }
                        }

                        foreach (var item in todaysBookings)
                        {
                            if (item.TimeslotId == SlotId)
                            {
                                var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                                var publicClient = root.clientManager.MakePublicClient();
                                var allTimeslots = await publicClient.GetTimeslotsAsync();
                                var allCourts = await publicClient.GetCourtsAsync();

                                TimeslotOut time;
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
                                                    var deletion = await EmployeeClient.DeleteGuestBookingAsync(item.Id);
                                                    if (deletion.Successful)
                                                    {
                                                        MessageBox.Show($"Buchung gelöscht:\nDatum: {item.Date}\nSpielfeld: {CourtName}" +
                                                            $"\nZeit: {time.Start.ToString()} - {time.End.ToString()}\nName {GuestName}", $"Buchung storniert");
                                                        GuestName = null;
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
                else if(IsClosing)
                {
                    var closings = await EmployeeClient.GetClosingsForDateAsync(Today);

                    if (closings.Successful)
                    {
                        var closingResults = closings.Result.ToList();

                        foreach (var close in closingResults)
                        {
                            if (close.Date == Today && close.CourtId == CourtId && close.StartTimeslotId <= SlotId && close.EndTimeslotId >= SlotId)
                            {
                                var result = await EmployeeClient.DeleteClosingAsync(close.Id);
                                if (result.Successful)
                                {
                                    var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                                    var publicClient = root.clientManager.MakePublicClient();
                                    var allTimeslots = await publicClient.GetTimeslotsAsync();
                                    TimeslotOut start = null, end = null;

                                    if(allTimeslots.Successful)
                                    {
                                        foreach(var slot in allTimeslots.Result.ToList())
                                        {
                                            if(slot.id == close.StartTimeslotId)
                                            {
                                                start = slot;
                                            }

                                            if(slot.id == close.EndTimeslotId)
                                            {
                                                end = slot;
                                            }
                                        }
                                        MessageBox.Show($"Feldsperrung gelöscht:\n\nDatum: {Today}\nSpielfeld: {CourtName}\nVon:{start?.Start} Bis: {end?.End}", "Feldsperrung gelöscht");
                                        await newCourtDefinitionTrigger.Invoke();
                                    }
                                }
                            }
                        }

                    }
                }
            });
        }

        public async void AddClosing(ClosingIn closing)
        {
            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();
            if (allTimeslots.Successful)
            {
                var slotList = allTimeslots.Result.ToList();
                string start = "", end;
                foreach (var slot in slotList)
                {
                    if(slot.id == closing.StartTimeslotId) 
                    {
                        start = slot.Start.ToString();
                    }

                    if(slot.id == closing.EndTimeslotId)
                    {
                        end = slot.End.ToString();

                        var response = await EmployeeClient.AddClosingAsync(closing);
                        if(response.Successful)
                        {
                            var newClosing = response.Result;
                            MessageBox.Show($"Feld sperren erfolgreich:\n\nDatum: {newClosing?.Date}\nSpielfeld {CourtName}\nVon: {start} Bis: {end}", "Feld gesperrt.");
                            empWindow.Close();
                            await newCourtDefinitionTrigger.Invoke();
                        }
                    }

                }
            }
        }


        public async void AddGuestbooking(GuestBookingIn guest)
        {
            var root = App.AppHost.Services.GetRequiredService<ClientManager>();
            var publicClient = root.clientManager.MakePublicClient();
            var allTimeslots = await publicClient.GetTimeslotsAsync();
            if (allTimeslots.Successful)
            {
                var slotList = allTimeslots.Result.ToList();
                foreach (var slot in slotList)
                {
                    if (slot.id == SlotId)
                    {
                        var response = await EmployeeClient.AddGuestBookingAsync(guest);
                        if (response.Successful)
                        {
                            var newUser = response.Result;
                            MessageBox.Show($"Gastbuchung erfolgreich:\n\nDatum: {newUser?.Date}\nSpielfeld {CourtName}\nVon: {slot.Start} Bis: {slot.End}\nName: {newUser?.GuestName}", "Gastbuchung erstellt.");
                            empWindow.Close();
                        }
                        break;
                    }
                }
            }
            GuestName = guest.GuestName;
            ChangeState(true);
        }

        public override void SetState()
        {
            SolidColorBrush green = (SolidColorBrush)new BrushConverter().ConvertFromString("#6f916f");
            SolidColorBrush red = (SolidColorBrush)new BrushConverter().ConvertFromString("#EE5C42");
            SolidColorBrush blue = (SolidColorBrush)new BrushConverter().ConvertFromString("#5F9EA0");
            SolidColorBrush yellow = (SolidColorBrush)new BrushConverter().ConvertFromString("#EEB422");

            if (GuestName != null)
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
            else if(IsClosing)
            {
                BackgroundColor = yellow;
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
