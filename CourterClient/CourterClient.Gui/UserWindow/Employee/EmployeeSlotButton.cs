using CourterClient.ApiClient;
using CourterClient.Gui.Gui.PopUpWindows;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
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
                if (!IsBooked && !IsClosing && !IsPast)
                {
                    var empWinVM = new EmployeePopUpViewModel(EmployeeClient, newGuestBooking, newClosing, Today, CourtName, CourtId, SlotId);
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
                                                    var deletion = await EmployeeClient.DeleteGuestBookingAsync(item.Id);
                                                    if (deletion.Successful)
                                                    {
                                                        info = new List<string>();
                                                        info.Add("Buchung gelöscht");
                                                        info.Add(item.Date.ToString());
                                                        info.Add(CourtName);
                                                        info.Add(time.Start.ToString());
                                                        info.Add(time.End.ToString());
                                                        var InfoView = new InfoView(info);
                                                        InfoView.ShowDialog();
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
                    var root = App.AppHost.Services.GetRequiredService<ClientManager>();
                    var publicClient = root.clientManager.MakePublicClient();
                    var closings = await publicClient.GetClosingsForDateAsync(Today);

                    if (closings.Successful)
                    {
                        var closingResults = closings.Result.ToList();

                        foreach (var close in closingResults)
                        {
                            if (close.Date == Today && close.CourtId == CourtId && close.StartTimeslotId <= SlotId && close.EndTimeslotId >= SlotId)
                            {
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
                                    List<string> info = new List<string>();
                                    info.Add("Sperrung löschen?");
                                    info.Add(Today.ToString());
                                    info.Add(CourtName);
                                    info.Add(start.Start.ToString());
                                    info.Add(end.End.ToString());

                                    var question = new DeleteView(info, transferResponse);
                                    question.ShowDialog();

                                    if(Response)
                                    {
                                        var result = await EmployeeClient.DeleteClosingAsync(close.Id);
                                        if (result.Successful)
                                        {


                                            info = new List<string>();
                                            info.Add("Feldsperrung gelöscht:");
                                            info.Add(Today.ToString());
                                            info.Add(CourtName);
                                            info.Add(start.Start.ToString());
                                            info.Add(end.End.ToString());
                                            var InfoView = new InfoView(info);
                                            InfoView.ShowDialog();
                                            await newCourtDefinitionTrigger.Invoke();
                                        }
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
                            
                            empWindow.Close();
                            List<string> info = new List<string>();
                            info.Add("Feld erfolgreich gesperrt:");
                            info.Add(newClosing.Date.ToString());
                            info.Add(CourtName);
                            info.Add(start);
                            info.Add(end);
                            var InfoView = new InfoView(info);
                            InfoView.ShowDialog();
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
                            empWindow.Close();
                            List<string> info = new List<string>();
                            info.Add($"Gastbuchung erstellt:");
                            info.Add(newUser.Date.ToString());
                            info.Add(CourtName);
                            info.Add(slot.Start.ToString());
                            info.Add(slot.End.ToString());
                            var InfoView = new InfoView(info);
                            InfoView.ShowDialog();
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
            SolidColorBrush green = (SolidColorBrush)new BrushConverter().ConvertFromString("#2E8B57");
            SolidColorBrush red = (SolidColorBrush)new BrushConverter().ConvertFromString("#EE5C42");
            SolidColorBrush blue = (SolidColorBrush)new BrushConverter().ConvertFromString("#1874CD");
            SolidColorBrush yellow = (SolidColorBrush)new BrushConverter().ConvertFromString("#FFC125");
            SolidColorBrush past = (SolidColorBrush)new BrushConverter().ConvertFromString("Transparent");

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
            else if(IsPast)
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

        public void CheckGuestname(List<BookingOut> todaysBookings, TimeSlot slot)
        {
            foreach (var item in todaysBookings)
            {
                if (item.TimeslotId == slot.Id)
                {
                    if (!IsPast)
                    {
                        if (item.GuestName != null)
                        {
                            GuestName = item.GuestName;
                        }
                        IsBooked = true;
                    }
                }
            }
        }
    }
}
