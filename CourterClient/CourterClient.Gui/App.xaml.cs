using CourterClient.Gui.CalendarWindow;
using CourterClient.Gui.Gui;
using CourterClient.Gui.Gui.AdminWindow;
using CourterClient.Gui.Gui.UserWindow;
using CourterClient.Gui.LoginWindow;
using CourterClient.Gui.RegistrationWindow;
using CourterClient.Gui.UserWindow;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Windows;

namespace CourterClient.Gui
{

    public partial class App : Application
    {
        public static IHost? AppHost { get; private set; }
        public static IServiceProvider? ServiceProvider { get; private set; }


        public App()
        {
            AppHost = Host.CreateDefaultBuilder()
                .ConfigureServices((hostContext, services) =>
                {
                    services.AddSingleton<LoginView>();
                    services.AddSingleton<RegistrationView>();
                    services.AddSingleton<UserView>();
                    services.AddSingleton<UserViewModel>();
                    services.AddSingleton<CalendarView>();
                    services.AddSingleton<AdminView>();
                    services.AddTransient<ClientManager>();
                })
                .Build();

            ServiceProvider = AppHost.Services;
        }

        protected override async void OnStartup(StartupEventArgs e)
        {
            var startupForm = AppHost!.Services.GetRequiredService<LoginView>();

            startupForm.Show();
            await AppHost!.StartAsync();

            base.OnStartup(e);
        }

        protected override async void OnExit(ExitEventArgs e)
        {
            await AppHost!.StopAsync();
            base.OnExit(e);
        }
    }
}
