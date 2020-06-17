import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";

import Applications from "./Applications";

const applications = [
    {
      "application_id": 1, 
      "application_statuses": [
        {
          "application_id": 1, 
          "application_status_id": 3, 
          "datetime_created": "Sat, 06 Jun 2020 03:36:13 GMT", 
          "experience_rating": "neutral", 
          "point_entry": {}, 
          "status": "Phone Interviewed"
        }, 
        {
          "application_id": 1, 
          "application_status_id": 10, 
          "datetime_created": "Sat, 23 May 2020 05:06:21 GMT", 
          "experience_rating": null, 
          "point_entry": {
            "application_id": null, 
            "application_status_id": 8, 
            "point_entry_id": 8, 
            "point_entry_type": "Update application status", 
            "point_entry_type_code": "uas"
          }, 
          "status": "Onsite interviewed"
        }
      ], 
      "datetime_applied": "Sat, 23 May 2020 03:36:10 GMT", 
      "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
      "job": {
        "company": {
          "company_id": 1, 
          "company_name": "My Company", 
          "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
          "website": "https://www.mycompany.com"
        }, 
        "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
        "job_id": 1, 
        "link": "https://www.linkedin.com/mycompany/software-engineer", 
        "source": "LinkedIn", 
        "title": "Software Engineer"
      }, 
      "journal_entries": [
        {
          "application_id": 1, 
          "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
          "entry": "This is a journal entry.", 
          "journal_entry_id": 1
        }, 
        {
          "application_id": 1, 
          "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
          "entry": "2nd journal entry to 1st application", 
          "journal_entry_id": 3
        }
      ], 
      "referred_by": "Anjelica", 
      "user_id": 1
    }, 
    {
      "application_id": 2, 
      "application_statuses": [
        {
          "application_id": 2, 
          "application_status_id": 2, 
          "datetime_created": "Thu, 28 May 2020 03:36:13 GMT", 
          "experience_rating": "positive", 
          "point_entry": {}, 
          "status": "Applied"
        }
      ], 
      "datetime_applied": "Thu, 28 May 2020 03:36:13 GMT", 
      "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
      "job": {
        "company": {
          "company_id": 2, 
          "company_name": "Another Company", 
          "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
          "website": "https://www.anothercompany.com"
        }, 
        "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
        "job_id": 2, 
        "link": "https://www.linkedin.com/anothercompany/software-engineer", 
        "source": "Glassdoor", 
        "title": "Software Engineer"
      }, 
      "journal_entries": [
        {
          "application_id": 2, 
          "datetime_created": "Sat, 23 May 2020 03:36:10 GMT", 
          "entry": "Another journal entry.", 
          "journal_entry_id": 2
        }
      ], 
      "referred_by": "Anjelica", 
      "user_id": 1
    }
  ]
let container = null;
beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
});
afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})

it("renders applications", () => {
    act(() => {
        render(<Applications 
            applications={applications}
            setApplications={() => {}}
            fetchUser={() => {}}
        />, container);
    });
    expect(container.textContent).toContain("Link: https://www.linkedin.com/mycompany/software-engineer");
    expect(container.textContent).toContain("Referred by: Anjelica");
    expect(container.textContent).toContain("Source: LinkedIn");
    expect(container.textContent).toContain("Software Engineer - Another Company");
})