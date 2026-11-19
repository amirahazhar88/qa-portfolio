export const NETWORK_ERROR_MESSAGE = "Unable to connect to the server";

// Normalize an API error into a RealWorld errors object ({ field: [messages] }).
// Errors without a usable response body (network failures, aborted requests,
// malformed JSON) are reported as a generic connectivity problem.
export const extractErrors = (error) => {
  if (
    error &&
    error.response &&
    error.response.data &&
    error.response.data.errors
  ) {
    return error.response.data.errors;
  }
  return { network: [NETWORK_ERROR_MESSAGE] };
};

export default extractErrors;
