select r.id, d.name, r.city, r.street, r.bldng, 
rp.report_timestamp, rp.text,
c.name, c.email
from reports r
left join distributor d on r.distributor_id = d.id
left join reports_parts rp on r.id = rp.id_reports
left join contacts c on c.id = d.contact_froneri_id
where 
rp.report_timestamp >= '2020-04-01 00:00:00' and
rp.report_timestamp < '2020-04-16 00:00:00'