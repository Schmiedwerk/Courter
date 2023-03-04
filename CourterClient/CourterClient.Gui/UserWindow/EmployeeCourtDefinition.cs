using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    public class EmployeeCourtDefinition : CourtDefinition
    {
        IEmployeeClient EmployeeClient { get; set; }

        public EmployeeCourtDefinition(IEmployeeClient employeeClient, string courtName, int id, List<TimeSlot> slots, DateOnly current) 
            : base(courtName, id, slots, current)
        {
            EmployeeClient = employeeClient;

            //await FillCourtSlots();
        }

        public async Task FillCourtSlots()
        {
            //SlotList = new ObservableCollection<SlotButtonData>();

            //for (int i = 0; i < Slots; i++)
            //{

            //    var button = new SlotButtonData(i, false, true, CourtName);
            //    SlotList.Add(button);
            //}
        }
    }
}
