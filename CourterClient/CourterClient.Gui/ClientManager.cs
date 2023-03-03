using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui
{
    public class ClientManager
    {
        private string _serverUrl = "http://localhost:8000";
        public RootClient clientManager;
        public ClientManager()
        {
            clientManager = new RootClient(_serverUrl);
        }
    }
}
