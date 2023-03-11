using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using CourterClient.ApiClient;

namespace CourterClient.Gui.Gui.AdminWindow
{
    internal class AdminViewModel : ViewModelBase
    {
        public TransferAdminCredentials adminTransfer;
        public TransferEmployeeCredentials employeeTransfer;
        public TransferCourtIn courtTransfer;
        public TransferTimeslotIn timeslotTransfer;

        private IAdminClient AdminClient { get; set;}
        private IPublicClient PublicClient { get; set;}

        private UserOut currentAdmin;
        private UserOut currentEmployee;
        private CourtOut currentCourt;
        private TimeslotOut currentTimeslot;

        private ObservableCollection<UserOut> admins = new ObservableCollection<UserOut>();

        private ObservableCollection<UserOut> employees = new ObservableCollection<UserOut>();

        private ObservableCollection<CourtOut> courts = new ObservableCollection<CourtOut>();

        private ObservableCollection<TimeslotOut> timeSlots = new ObservableCollection<TimeslotOut>();

        public UserOut CurrentAdmin
        {
            get => currentAdmin;
            set
            {
                if(currentAdmin != value)
                {
                    currentAdmin = value;
                    this.RaisePropertyChanged();
                }
            }
        }
        
        public UserOut CurrentEmployee
        {
            get => currentEmployee;
            set
            {
                if (currentEmployee != value)
                {
                    currentEmployee = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public CourtOut CurrentCourt
        {
            get => currentCourt;
            set
            {
                if (currentCourt != value)
                {
                    currentCourt = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public TimeslotOut CurrentTimeslot
        {
            get => currentTimeslot;
            set
            {
                if(currentTimeslot != value)
                {
                    currentTimeslot = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<UserOut> Admins
        {
            get => admins;
            set
            {
                if (admins != value)
                {
                    admins = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<UserOut> Employees
        {
            get => employees;
            set
            {
                if (employees != value)
                {
                    employees = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<CourtOut> Courts
        {
            get => courts;
            set
            {
                if (courts != value)
                {
                    courts = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ObservableCollection<TimeslotOut> TimeSlots
        {
            get => timeSlots;
            set
            {
                if (timeSlots != value)
                {
                    timeSlots = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public ICommand CreateAdminAccount => new DelegateCommand(_ =>
        {
            var create = new CreateUser(adminTransfer);
            create.ShowDialog();
        });
        public ICommand CreateEmployeeAccount => new DelegateCommand(_ =>
        {
            var create = new CreateUser(employeeTransfer);
            create.ShowDialog();
        });
        public ICommand DeleteEmployeeAccount => new DelegateCommand(async _ =>
        {
            UserOut user = CurrentEmployee;

            if (user != null)
            {
                var response = await AdminClient.DeleteEmployeeAsync(user.Id);
            }

            await GetEmployees();
        });
        public ICommand CreateNewCourt => new DelegateCommand(_ =>
        {
            var newCourt = new CreateCourt(courtTransfer);
            newCourt.ShowDialog();
        });

        public ICommand CreateNewTimeslot => new DelegateCommand(_ =>
        {
            var newTimeslot = new CreateTime(timeslotTransfer);
            newTimeslot.ShowDialog();
        });

        public ICommand DeleteAdminAccount => new DelegateCommand(async _ =>
        {
            UserOut user = CurrentAdmin;

            if (user != null)
            {
                var response = await AdminClient.DeleteAdminAsync(user.Id);
            }

            await GetAdmins();
        });

        public ICommand DeleteCourt => new DelegateCommand(async _ => 
        {
            CourtOut court = CurrentCourt;

            if(court != null )
            {
                var response = await AdminClient.DeleteCourtAsync(court.id);
            }
            await GetCourts();
        });

        public ICommand DeleteTimeslot => new DelegateCommand(async _ =>
        {
            TimeslotOut slot = CurrentTimeslot;

            if (slot != null)
            {
                var response = await AdminClient.DeleteTimeslotAsync(slot.id);
            }
            await GetTimeslots();
        });

        public AdminViewModel(IPublicClient publicClient, IAdminClient adminClient)
        {
            PublicClient = publicClient;
            AdminClient = adminClient;

            this.adminTransfer += new TransferAdminCredentials(CreateAdmin);
            this.employeeTransfer += new TransferEmployeeCredentials(CreateEmployee);
            this.courtTransfer += new TransferCourtIn(CreateCourt);
            this.timeslotTransfer += new TransferTimeslotIn(CreateTimeslot);
        }

        public async Task FillTables()
        {
            var adminTask = GetAdmins();
            var employeeTask = GetEmployees();
            var courtTask = GetCourts();
            var timeslotTask = GetTimeslots();

            await Task.WhenAll(adminTask, employeeTask, courtTask, timeslotTask);
        }

        public async Task GetAdmins()
        {
            var adminList = await AdminClient.GetAdminsAsync();

            if(adminList.Successful)
            {
                List<UserOut> users = adminList.Result.ToList();
                
                this.Admins = new ObservableCollection<UserOut>();
                foreach (var item in users)
                {
                    this.Admins.Add(item);
                }
            }
        }

        public async Task GetEmployees()
        {
            var employeeList = await AdminClient.GetEmployeesAsync();

            if (employeeList.Successful)
            {
                List<UserOut> users = employeeList.Result.ToList();

                this.Employees = new ObservableCollection<UserOut>();
                foreach (var item in users)
                {
                    this.Employees.Add(item);
                }
            }
        }

        public async Task GetCourts()
        {
            var courtList = await PublicClient.GetCourtsAsync();

            if (courtList.Successful)
            {
                List<CourtOut> users = courtList.Result.ToList();

                this.Courts = new ObservableCollection<CourtOut>();
                foreach (var item in users)
                {
                    this.Courts.Add(item);
                }
            }
        }

        public async Task GetTimeslots()
        {
            var timeslotList = await PublicClient.GetTimeslotsAsync();

            if (timeslotList.Successful)
            {
                List<TimeslotOut> users = timeslotList.Result.ToList();

                this.TimeSlots = new ObservableCollection<TimeslotOut>();
                foreach (var item in users)
                {
                    this.TimeSlots.Add(item);
                }
            }
        }

        public async void CreateAdmin(Credentials user)
        {
            var response = await AdminClient.AddAdminAsync(user);

            if(response.Successful)
            {
                var newUser = response.Result;
                MessageBox.Show($"Admin: {newUser?.Username}\nid: {newUser?.Id} \nErfolgreich erstellt!", "Admin erstellt!");
                await GetAdmins();
            }
            else
            {
                MessageBox.Show($"Erstellen fehlgeschlagen: \n{response.Detail}", "Erstellen fehlgeschlagen.");
            }
        }

        public async void CreateEmployee(Credentials user)
        {
            var response = await AdminClient.AddEmployeeAsync(user);

            if (response.Successful)
            {
                var newUser = response.Result;
                MessageBox.Show($"Mitarbeiter: {newUser?.Username}\nid: {newUser?.Id} \nErfolgreich erstellt!", "Mitarbeiter erstellt!");
                await GetEmployees();
            }
            else
            {
                MessageBox.Show($"Erstellen fehlgeschlagen: \n{response.Detail}", "Erstellen fehlgeschlagen.");
            }
        }

        public async void CreateCourt(CourtIn court)
        {
            var response = await AdminClient.AddCourtAsync(court);

            if(response.Successful)
            {
                var newCourt = response.Result;
                MessageBox.Show($"Feld: {newCourt?.Name}\nUntergrund: {newCourt?.Surface} \nErfolgreich erstellt!", "Feld erstellt!");
                await GetCourts();
            }
        }

        public async void CreateTimeslot(TimeslotIn timeslot)
        {
            var response = await AdminClient.AddTimeslotAsync(timeslot);

            if (response.Successful)
            {
                var newTime = response.Result;
                MessageBox.Show($"Neues Zeitfenster mit \nStartzeit: {newTime?.Start}\nEnde: {newTime?.End} \nErfolgreich erstellt!", "Zeitfenster erstellt!");
                await GetTimeslots();
            }
            else
            {
                MessageBox.Show($"Erstellen fehlgeschlagen:\n{response.Detail}", "Erstellen fehlgeschlagen!");
            }
        }
    }
}
