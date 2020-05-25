import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";

import ApplicationForm from "./ApplicationForm";

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

it("renders application form", () => {
    act(() => {
        render(<ApplicationForm 
            handleChange={() => {}}
            handleSubmit={() => {}} 
            inputs={{
                title: '',
                link: '',
                source: '',
                company_name: '',
                website: '',
                status: '',
            }} 
            setInput={() => {}}
            initialInputs={{
                title: '',
                link: '',
                source: '',
                company_name: '',
                website: '',
                status: '',
            }}
        />, container);
    });
    expect(container.textContent).toContain("Enter new application:");

})