document.addEventListener('DOMContentLoaded', () => {
    // Select elements from the form for real-time fee calculations
    const form = document.querySelector('form');
    const totalField = document.getElementById('totalFees');
    const breakdownList = document.getElementById('breakdownList');

    // Object with prices for each option (consistent with backend values)
    const prices = {
        nursery: 6500,
        grade_1_3: 8500,
        grade_4_6: 9000,
        grade_7_9: 1200,
        food: 3500,
        two_way_town: 7000,
        two_way_uma: 8000,
        one_way: 4500,
        admission: 1000,
        interview: 1000,
        diary: 150,
        activity_fee: 200,
        exercise_books: 500,
        text_books: 6000,
        assessment_tool: 300,
        uniform: 1800,
        track_suit: 1800,
        tshirt: 450,
        jumper: 2000,
        jss_jumper: 2500
    };

    // Calculate and update the fee total and breakdown in real-time
    const calculateFees = () => {
        let total = 0;
        let breakdown = [];

        // Get selected grade and add corresponding fee
        const grade = form.grade.value;
        if (prices[grade]) {
            total += prices[grade];
            breakdown.push({ item: 'School Fee', cost: prices[grade] });
        }

        // Check each optional field and add to total if selected
        const optionalFields = ['food', 'admission', 'interview', 'diary', 'activity_fee', 'exercise_books', 'text_books', 'assessment_tool', 'uniform', 'track_suit', 'tshirt', 'jumper', 'jss_jumper'];
        optionalFields.forEach(field => {
            if (form[field] && form[field].checked) {
                total += prices[field];
                breakdown.push({ item: field.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()), cost: prices[field] });
            }
        });

        // Transport option (non-checkbox, so checked with value)
        const transport = form.transport.value;
        if (transport !== 'none' && prices[transport]) {
            total += prices[transport];
            breakdown.push({ item: 'Transport', cost: prices[transport] });
        }

        // Update the UI with the calculated total and breakdown
        totalField.textContent = `Total: ${total} USD`;
        breakdownList.innerHTML = ''; // Clear previous entries
        breakdown.forEach(entry => {
            const listItem = document.createElement('li');
            listItem.textContent = `${entry.item}: ${entry.cost} USD`;
            breakdownList.appendChild(listItem);
        });
    };

    // Add event listeners for any changes in the form to recalculate fees
    form.addEventListener('change', calculateFees);
    calculateFees(); // Initial calculation on page load
});
