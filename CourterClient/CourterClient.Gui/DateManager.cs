using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui
{
    public class DateManager : ViewModelBase
    {
        DateOnly current;
        public DateOnly Current
        {
            get => current;
            set
            {
                if (value != current)
                {
                    current = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        string currentToString;
        public string CurrentToString
        {   
            get => currentToString;
            set
            {
                if (value != currentToString)
                {
                    currentToString = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        DateOnly previous;
        public DateOnly Previous
        {
            get => previous;
            set
            {
                if (value != previous)
                {
                    previous = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        string previousToString;
        public string PreviousToString
        {
            get => previousToString;
            set
            {
                if (value != previousToString)
                {
                    previousToString = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        DateOnly next;
        public DateOnly Next
        {
            get => next;
            set
            {
                if (value != next)
                {
                    next = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        string nextToString;
        public string NextToString
        {
            get => nextToString;
            set
            {
                if (value != nextToString)
                {
                    nextToString = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public DateManager()
        {
            var today = DateOnly.FromDateTime(DateTime.Today);
            
            SetDate(today);
        }

        public void SetDate(DateOnly date)
        {
            this.Current = date;
            this.Previous = date.AddDays(-1);
            this.Next = date.AddDays(1);

            this.CurrentToString = $"{Current.DayOfWeek}, {Current.ToString("d MMM")}";
            this.PreviousToString = $"{Previous.DayOfWeek}, {Previous.ToString("d MMM")}";
            this.NextToString = $"{Next.DayOfWeek}, {Next.ToString("d MMM")}";
        }
    }
}
 