namespace CourterClient.ApiClient;

public interface IPublicClient
{
	Task<ApiResponse<IEnumerable<CourtOut>>> GetCourtsAsync();
	Task<ApiResponse<IEnumerable<TimeslotOut>>> GetTimeslotsAsync();
}
