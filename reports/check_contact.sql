select d.name, c.name, c.email
from distributor d 
left join contacts c on c.id = d.contact_froneri_id