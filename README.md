# Inventory Management

The main goal of this project is to help in the balance the trade off between the two most important questions in the supply chain management, When to Buy? and Howmuch to Buy ?

If you have the prediction of the item unit price for the next 6 months, and you have a specific inventory size, and you already know what will be your quantity need for these 6 months through your PRs and POs. Should you buy all what you need in the first month? or buy in a month what you need now ?

This tool will help you optimize the quantity and the time because you are restricted to some constraints:


1. Inventory Size
2. Storage Cost : You pay for the rent of the storage , security , electricity , facilities  (you will distribute the storage cost on the unit price of the item)
3. Handling Cost : Transportation for example
4. Taxes & Insurance 
5. Damage & Theft : Or any risk related to the item, it is a percentage of the total quantity  
6. Order Cost : it is like a discount if you ordered a bulk quantity
7. Purchase Cost : Some costs that are related to the POs and inspections

And we need to return the present value of all the months to compare the different results of the model as an apple to an apple

If you buy all the quantity early you will pay storage,damage costs for the 6 months, plus the opportunity cost for your money that are stuck in the material
and If you buy month by month, You will pay extra Purchase, Handling, and Order Costs

So there must be the optimum point wich reduce the the cost to its minimal

### Inputs of the project :
1.assumptions (CSV file)
2.Predicted Prices and Quantity (CSV file)

### Outputs of the project :
1.results (CSV File) : that determines the optimum quantity per month


* You can use the Excel sheet (inventory_management) for your manual trials, but don't forget to match the unit prices between inventory_management and predicted prices



