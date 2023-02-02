using System;
using Newtonsoft.Json;

namespace CourterClient.ApiClient;

public record Credentials(
    [property: JsonProperty("username")] string Username,
    [property: JsonProperty("password")] string Password
);

public record UserOut(
    [property: JsonProperty("id")] int Id,
    [property: JsonProperty("username")] string Username
);

public record CourtIn(
    [property: JsonProperty("name")] string Name,
    [property: JsonProperty("surface")] string? Surface
);

public record CourtOut(
    string Name,
    string? Surface,
    [property: JsonProperty("id")] int id
) : CourtIn(Name, Surface);

public record TimeslotIn(
    [property: JsonProperty("start")] TimeOnly Start,
    [property: JsonProperty("end")] TimeOnly End
);

public record TimeslotOut(
    TimeOnly Start,
    TimeOnly End,
    [property: JsonProperty("id")] int id
) : TimeslotIn(Start, End);

public record CustomerBookingIn(
    [property: JsonProperty("date")] DateOnly Date,
    [property: JsonProperty("timeslot_id")] int TimeslotId,
    [property: JsonProperty("court_id")] int CourtId
);

public record GuestBookingIn(
    DateOnly Date,
    int TimeslotId,
    int CourtId,
    [property: JsonProperty("guest_name")] string GuestName
) : CustomerBookingIn(Date, TimeslotId, CourtId);

public record BookingOut(
    DateOnly Date,
    int TimeslotId,
    int CourtId,
    [property: JsonProperty("id")] int Id,
    [property: JsonProperty("guest_name")] string? GuestName,
    [property: JsonProperty("customer_id")] int? CustomerId
) : CustomerBookingIn(Date, TimeslotId, CourtId);

public record ClosingIn(
    [property: JsonProperty("date")] DateOnly Date,
    [property: JsonProperty("start_timeslot_id")] int StartTimeslotId,
    [property: JsonProperty("end_timeslot_id")] int EndTimeslotId,
    [property: JsonProperty("court_id")] int CourtId
);

public record ClosingOut(
    DateOnly Date,
    int StartTimeslotId,
    int EndTimeslotId,
    int CourtId,
    [property: JsonProperty("id")] int Id
) : ClosingIn(Date, StartTimeslotId, EndTimeslotId, CourtId);
